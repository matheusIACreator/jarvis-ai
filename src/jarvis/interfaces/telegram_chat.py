"""Chat with Jarvis by Telegram message, in a background thread.

Only messages from the configured chat (the user's own) are answered; anything else is
ignored. Message text reaches the model as the user's request (role "user"), never as
system instructions. Messages sent while Jarvis was offline are skipped at startup.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

from jarvis.interfaces.telegram import TelegramError

WELCOME = "At your service, sir. Send me a message whenever you need something."
RETRY_SECONDS = 5.0


class TelegramChat:
    def __init__(
        self,
        bot: Any,  # TelegramBot, or a test double with the same methods
        chat_id: str | int,
        reply: Callable[[str], str],  # the brain for this channel
        log: Callable[[str], None] = print,
    ) -> None:
        self.bot = bot
        self.chat_id = str(chat_id)
        self.reply = reply
        self.log = log
        self.offset: int | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def skip_backlog(self) -> int:
        """Mark every message already waiting as handled. Returns how many were skipped."""
        updates = self.bot.get_updates(offset=-1, poll_seconds=0)
        if updates:
            self.offset = updates[-1]["update_id"] + 1
        return len(updates)

    def handle(self, update: dict) -> None:
        """Answer one update if it is a text message from the user's chat."""
        self.offset = update["update_id"] + 1
        message = update.get("message") or {}
        chat_id = str((message.get("chat") or {}).get("id"))
        text = (message.get("text") or "").strip()
        if chat_id != self.chat_id:
            if message:
                self.log(f"(Telegram: ignored a message from unknown chat {chat_id})")
            return
        if not text:
            return
        if text == "/start":
            self.bot.send_message(self.chat_id, WELCOME)
            return
        self.log(f"telegram you> {text}")
        try:
            self.bot.send_typing(self.chat_id)
        except TelegramError:
            pass  # cosmetic only
        answer = self.reply(text) or "Noted, sir."
        self.log(f"telegram jarvis> {answer}")
        self.bot.send_message(self.chat_id, answer)

    def poll_once(self) -> None:
        for update in self.bot.get_updates(offset=self.offset):
            try:
                self.handle(update)
            except Exception as exc:  # one bad message must not stop the channel
                self.log(f"(Telegram: failed to answer: {type(exc).__name__}: {exc})")

    def run(self) -> None:
        try:
            skipped = self.skip_backlog()
            if skipped:
                self.log(f"(Telegram: skipped {skipped} message(s) sent while I was offline)")
        except Exception as exc:
            self.log(f"(Telegram: could not skip old messages: {type(exc).__name__}: {exc})")
        while not self._stop.is_set():
            try:
                self.poll_once()
            except Exception as exc:  # never let the channel die silently
                self.log(f"(Telegram: {type(exc).__name__}: {exc}; retrying in {RETRY_SECONDS:g} s)")
                self._stop.wait(RETRY_SECONDS)

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run, name="telegram-chat", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
