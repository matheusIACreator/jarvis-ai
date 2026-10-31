"""Send a Telegram message to the user's own chat, only after he confirms by voice."""

from __future__ import annotations

from collections.abc import Callable

from jarvis.confirmation import ConfirmationGate, PendingAction
from jarvis.tools.base import Tool

SENT = "Sent to your Telegram, sir."


def make_telegram_tool(gate: ConfirmationGate, send: Callable[[str], None]) -> Tool:
    """`send(text)` delivers to the configured chat; it only runs after a spoken yes."""

    def send_telegram_message(text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError("The message is empty.")

        def execute() -> str:
            send(text)
            return SENT

        gate.request(
            PendingAction(description=f"send \"{text}\" to the user's Telegram", execute=execute)
        )
        return f'Shall I send "{text}" to your Telegram?'

    return Tool(
        name="send_telegram_message",
        description=(
            "Sends a text message to the user's own Telegram chat (notes, reminders, links, "
            "summaries for himself). It cannot message other people. The message is not sent "
            "until the user confirms out loud. Call this tool BEFORE asking for confirmation; "
            "its result is the confirmation question the application will speak directly."
        ),
        input_schema={
            "type": "object",
            "properties": {"text": {"type": "string", "description": "The exact message to send."}},
            "required": ["text"],
            "additionalProperties": False,
        },
        handler=send_telegram_message,
        reply_directly=True,
    )
