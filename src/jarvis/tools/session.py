"""Let the model close the voice session when the user is done talking."""

from __future__ import annotations

from collections.abc import Callable

from jarvis.tools.base import Tool


def make_end_conversation_tool(on_end: Callable[[], None]) -> Tool:
    def end_conversation() -> str:
        on_end()
        return "Session closed."

    return Tool(
        name="end_conversation",
        description=(
            "Ends the voice session so Jarvis stops listening until the next double clap. "
            "Call it when the user signals he is done (thanks him for nothing further, says "
            "that's all, goodbye, good night). Write your brief farewell as text in the same reply."
        ),
        input_schema={"type": "object", "properties": {}, "additionalProperties": False},
        handler=end_conversation,
        final=True,
    )
