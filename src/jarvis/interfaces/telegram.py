"""Minimal Telegram Bot API client using only the standard library.

The bot token is part of every request URL, so errors are re-raised without the URL and
nothing here logs requests.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

API = "https://api.telegram.org"
MAX_MESSAGE_LENGTH = 4096


class TelegramError(RuntimeError):
    pass


class TelegramBot:
    def __init__(self, token: str, timeout: float = 15.0) -> None:
        self._token = token
        self.timeout = timeout

    def __repr__(self) -> str:
        return "TelegramBot(token=***)"

    def call(self, method: str, timeout: float | None = None, **params: Any) -> Any:
        request = urllib.request.Request(
            f"{API}/bot{self._token}/{method}",
            data=json.dumps(params).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout or self.timeout) as response:
                body = json.load(response)
        except urllib.error.HTTPError as exc:
            description = _description(exc)
            raise TelegramError(f"Telegram {method} failed ({exc.code}): {description}") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise TelegramError(f"Telegram {method} failed: {type(exc).__name__}") from None
        if not body.get("ok"):
            raise TelegramError(f"Telegram {method} failed: {body.get('description')}")
        return body["result"]

    def send_message(self, chat_id: str | int, text: str) -> None:
        if not text.strip():
            raise ValueError("Message text is empty.")
        self.call("sendMessage", chat_id=chat_id, text=text[:MAX_MESSAGE_LENGTH])

    def send_typing(self, chat_id: str | int) -> None:
        self.call("sendChatAction", chat_id=chat_id, action="typing")

    def get_updates(self, offset: int | None = None, poll_seconds: int = 25) -> list[dict]:
        """Long-poll for new updates; returns as soon as one arrives or after `poll_seconds`."""
        params: dict[str, Any] = {"timeout": poll_seconds, "allowed_updates": ["message"]}
        if offset is not None:
            params["offset"] = offset
        return self.call("getUpdates", timeout=poll_seconds + 10, **params)


def _description(exc: urllib.error.HTTPError) -> str:
    try:
        return json.load(exc).get("description", "")
    except Exception:
        return ""
