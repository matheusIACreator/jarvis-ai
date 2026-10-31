from types import SimpleNamespace

from jarvis.brain.assistant import (
    FALLBACK_REPLY,
    MAX_TURNS_KEPT,
    MODEL,
    SYSTEM_PROMPT,
    Assistant,
)
from jarvis.tools.base import Tool, ToolRegistry


def text(value):
    return SimpleNamespace(type="text", text=value)


def thinking():
    return SimpleNamespace(type="thinking", thinking="", signature="sig")


def tool_use(name, tool_input, block_id="toolu_1"):
    return SimpleNamespace(type="tool_use", name=name, input=tool_input, id=block_id)


def response(stop_reason, *content):
    return SimpleNamespace(stop_reason=stop_reason, content=list(content))


class FakeClient:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        self.messages = self

    def create(self, **kwargs):
        # Snapshot: the assistant keeps appending to the same list.
        self.requests.append({**kwargs, "messages": list(kwargs["messages"])})
        return self.responses.pop(0)


def registry():
    tool = Tool(
        "get_current_datetime",
        "Clock.",
        {"type": "object", "properties": {}},
        lambda: "Saturday, 2026-10-31 21:05",
    )
    return ToolRegistry([tool])


def test_plain_reply_and_request_shape():
    client = FakeClient(response("end_turn", thinking(), text("Good evening, sir.")))
    assistant = Assistant(client=client, tools=registry())
    assert assistant.reply("Hello") == "Good evening, sir."

    request = client.requests[0]
    assert request["model"] == MODEL
    assert request["system"][0]["text"] == SYSTEM_PROMPT
    assert request["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert request["tools"][0]["name"] == "get_current_datetime"
    assert "temperature" not in request
    assert request["messages"] == [{"role": "user", "content": "Hello"}]


def test_tool_round_trip_keeps_assistant_content_unchanged():
    first = response("tool_use", thinking(), tool_use("get_current_datetime", {}))
    client = FakeClient(first, response("end_turn", text("It is Saturday, sir.")))
    assistant = Assistant(client=client, tools=registry())

    assert assistant.reply("What day is it?") == "It is Saturday, sir."
    second_request = client.requests[1]["messages"]
    assert second_request[1] == {"role": "assistant", "content": first.content}
    assert second_request[2]["content"] == [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_1",
            "content": "Saturday, 2026-10-31 21:05",
            "is_error": False,
        }
    ]


def test_parallel_tool_calls_answered_in_one_message():
    first = response(
        "tool_use",
        tool_use("get_current_datetime", {}, "a"),
        tool_use("missing_tool", {}, "b"),
    )
    client = FakeClient(first, response("end_turn", text("Done.")))
    Assistant(client=client, tools=registry()).reply("Two things")
    results = client.requests[1]["messages"][2]["content"]
    assert [r["tool_use_id"] for r in results] == ["a", "b"]
    assert results[1]["is_error"] is True


def test_history_keeps_only_text_of_finished_turns():
    first = response("tool_use", thinking(), tool_use("get_current_datetime", {}))
    client = FakeClient(
        first,
        response("end_turn", text("Saturday, sir.")),
        response("end_turn", text("You're welcome.")),
    )
    assistant = Assistant(client=client, tools=registry())
    assistant.reply("What day is it?")
    assistant.reply("Thanks")
    assert client.requests[2]["messages"] == [
        {"role": "user", "content": "What day is it?"},
        {"role": "assistant", "content": "Saturday, sir."},
        {"role": "user", "content": "Thanks"},
    ]


def test_history_is_trimmed():
    replies = [response("end_turn", text(f"r{i}")) for i in range(MAX_TURNS_KEPT + 3)]
    assistant = Assistant(client=FakeClient(*replies), tools=registry())
    for i in range(MAX_TURNS_KEPT + 3):
        assistant.reply(f"q{i}")
    assert len(assistant.history) == 2 * MAX_TURNS_KEPT
    assert assistant.history[-1] == {"role": "assistant", "content": f"r{MAX_TURNS_KEPT + 2}"}


def test_refusal_gives_fallback():
    client = FakeClient(response("refusal"))
    assert Assistant(client=client, tools=registry()).reply("...") == FALLBACK_REPLY


def test_endless_tool_use_stops():
    loops = [response("tool_use", tool_use("get_current_datetime", {})) for _ in range(10)]
    client = FakeClient(*loops)
    assert Assistant(client=client, tools=registry()).reply("loop") == FALLBACK_REPLY
    assert len(client.requests) == 6
