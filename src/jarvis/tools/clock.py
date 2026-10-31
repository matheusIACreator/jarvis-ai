"""Current local date and time.

Kept as a tool instead of being written into the system prompt: a timestamp in the prompt
would change every request and break prompt caching.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from jarvis.tools.base import Tool


def make_clock_tool(now: Callable[[], datetime] = lambda: datetime.now().astimezone()) -> Tool:
    def get_current_datetime() -> str:
        current = now()
        return current.strftime("%A, %Y-%m-%d %H:%M (UTC%z)")

    return Tool(
        name="get_current_datetime",
        description=(
            "Returns the user's current local date, weekday and time. "
            "Use it whenever the answer depends on today's date or the time; never guess them."
        ),
        input_schema={"type": "object", "properties": {}, "additionalProperties": False},
        handler=get_current_datetime,
    )
