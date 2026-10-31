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

        return gate.request(
            PendingAction(description=f'send "{text}" to your Telegram', execute=execute)
        )

    return Tool(
        name="send_telegram_message",
        description=(
            "Sends a text message to the user's own Telegram chat (notes, reminders, links, "
            "summaries for himself). It cannot message other people. The message is not sent "
            "until the user confirms out loud, so after calling it, read the message back and "
            "ask him to confirm."
        ),
        input_schema={
            "type": "object",
            "properties": {"text": {"type": "string", "description": "The exact message to send."}},
            "required": ["text"],
            "additionalProperties": False,
        },
        handler=send_telegram_message,
    )
