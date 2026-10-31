from datetime import datetime, timedelta, timezone

import pytest

from jarvis.tools.base import Tool, ToolRegistry
from jarvis.tools.clock import make_clock_tool


def echo_tool(name="echo"):
    return Tool(
        name=name,
        description="Echo text.",
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
        handler=lambda text: text,
    )


def test_definitions_are_sorted_and_plain():
    registry = ToolRegistry([echo_tool("zeta"), echo_tool("alpha")])
    definitions = registry.definitions()
    assert [d["name"] for d in definitions] == ["alpha", "zeta"]
    assert set(definitions[0]) == {"name", "description", "input_schema"}


def test_duplicate_names_are_rejected():
    with pytest.raises(ValueError):
        ToolRegistry([echo_tool(), echo_tool()])


def test_run_calls_handler():
    result = ToolRegistry([echo_tool()]).run("echo", {"text": "hi"})
    assert result.content == "hi"
    assert not result.is_error


def test_unknown_tool_is_an_error_result():
    result = ToolRegistry().run("nope", {})
    assert result.is_error


def test_failing_handler_becomes_error_result():
    def boom():
        raise RuntimeError("broken")

    tool = Tool("boom", "Fails.", {"type": "object", "properties": {}}, boom)
    result = ToolRegistry([tool]).run("boom", {})
    assert result.is_error
    assert "broken" in result.content


def test_bad_arguments_become_error_result():
    result = ToolRegistry([echo_tool()]).run("echo", {"wrong": 1})
    assert result.is_error


def test_clock_tool_formats_local_time():
    fixed = datetime(2026, 10, 31, 21, 5, tzinfo=timezone(timedelta(hours=-3)))
    tool = make_clock_tool(now=lambda: fixed)
    assert tool.handler() == "Saturday, 2026-10-31 21:05 (UTC-0300)"
