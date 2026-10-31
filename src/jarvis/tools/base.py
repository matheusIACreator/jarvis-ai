"""The single contract every Jarvis tool follows.

The brain only sees `ToolRegistry`: tool definitions to send to the model and a way to run a
call by name. How a tool does its work stays inside the tool.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    input_schema: Mapping[str, Any]
    handler: Callable[..., str]
    # A final tool ends the turn: it runs, and the text already written is the reply,
    # with no follow-up request to the model.
    final: bool = False
    # A successful result is already user-facing text (e.g. a prepared confirmation question).
    reply_directly: bool = False

    def definition(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": dict(self.input_schema),
        }


@dataclass(frozen=True)
class ToolResult:
    content: str
    is_error: bool = False


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            if tool.name in self._tools:
                raise ValueError(f"Duplicate tool name: {tool.name}")
            self._tools[tool.name] = tool

    def definitions(self) -> list[dict[str, Any]]:
        # Sorted so the request prefix stays byte-identical and prompt caching keeps working.
        return [self._tools[name].definition() for name in sorted(self._tools)]

    def is_final(self, name: str) -> bool:
        tool = self._tools.get(name)
        return tool is not None and tool.final

    def replies_directly(self, name: str) -> bool:
        tool = self._tools.get(name)
        return tool is not None and tool.reply_directly

    def run(self, name: str, tool_input: Mapping[str, Any]) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(f"Unknown tool: {name}", is_error=True)
        try:
            return ToolResult(tool.handler(**tool_input))
        except Exception as exc:  # A failing tool must not crash the voice loop.
            return ToolResult(f"{type(exc).__name__}: {exc}", is_error=True)
