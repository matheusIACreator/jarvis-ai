import io
import json
import urllib.error

import pytest

from jarvis.confirmation import CANCELLED, FAILED, ConfirmationGate, PendingAction, classify
from jarvis.conversation import Conversation
from jarvis.interfaces import telegram
from jarvis.interfaces.telegram import TelegramBot, TelegramError
from jarvis.tools.base import ToolRegistry
from jarvis.tools.telegram import SENT, make_telegram_tool


@pytest.mark.parametrize("text", ["Yes.", "Yes, please", "send it", "Go ahead!", "yeah", "Yes, Jarvis."])
def test_clear_yes(text):
    assert classify(text) == "yes"


@pytest.mark.parametrize("text", ["No.", "No, don't send it", "Cancel", "Wait", "never mind", "Don't."])
def test_clear_no(text):
    assert classify(text) == "no"


@pytest.mark.parametrize(
    "text",
    ["Yes, but change it to eight", "What did you say?", "Make it shorter", "yes no", "I guess"],
)
def test_anything_else_is_unclear(text):
    assert classify(text) == "unclear"


def pending(log):
    def execute():
        log.append("sent")
        return "Done, sir."

    return PendingAction("send a test", execute)


def test_yes_executes_once():
    gate, log = ConfirmationGate(), []
    gate.request(pending(log))
    resolution = gate.resolve("Yes")
    assert resolution.reply == "Done, sir."
    assert "carried it out" in resolution.record and "send a test" in resolution.record
    assert log == ["sent"]
    assert gate.resolve("Yes") is None  # nothing pending any more
    assert log == ["sent"]


def test_no_cancels_without_executing():
    gate, log = ConfirmationGate(), []
    gate.request(pending(log))
    resolution = gate.resolve("No, thanks")
    assert resolution.reply == CANCELLED
    assert "declined" in resolution.record
    assert log == []


def test_unclear_cancels_and_passes_text_on():
    gate, log = ConfirmationGate(), []
    gate.request(pending(log))
    assert gate.resolve("Yes, but change it") is None
    assert gate.pending is None
    assert log == []


def test_failure_is_reported_not_raised():
    gate = ConfirmationGate()

    def boom():
        raise RuntimeError("network down")

    gate.request(PendingAction("send", boom))
    resolution = gate.resolve("yes")
    assert resolution.reply == FAILED
    assert "failed" in resolution.record


def test_request_message_tells_model_it_is_not_done():
    message = ConfirmationGate().request(PendingAction("send 'hi'", lambda: ""))
    assert message.startswith("NOT DONE YET")


def test_telegram_tool_only_sends_after_yes():
    gate, sent = ConfirmationGate(), []
    registry = ToolRegistry([make_telegram_tool(gate, sent.append)])
    result = registry.run("send_telegram_message", {"text": "Buy milk"})
    assert not result.is_error
    assert "Buy milk" in result.content
    assert sent == []
    assert gate.resolve("Yes, send it").reply == SENT
    assert sent == ["Buy milk"]


def test_telegram_tool_rejects_empty_text():
    registry = ToolRegistry([make_telegram_tool(ConfirmationGate(), lambda text: None)])
    assert registry.run("send_telegram_message", {"text": "  "}).is_error


def test_conversation_routes_answer_to_gate_before_brain():
    gate, sent, said, thought = ConfirmationGate(), [], [], []
    gate.request(PendingAction("send", lambda: sent.append(1) or "Sent."))
    heard = ["Yes", "What time is it?"]
    Conversation(
        listen=lambda: heard.pop(0) if heard else "",
        think=lambda text: thought.append(text) or "Noon.",
        say=said.append,
        confirm=lambda text: (r := gate.resolve(text)) and r.reply,
    ).run()
    assert sent == [1]
    assert said == ["Sent.", "Noon."]
    assert thought == ["What time is it?"]


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_bot_sends_json_and_hides_token(monkeypatch):
    requests = []

    def fake_urlopen(request, timeout):
        requests.append(request)
        return FakeResponse(json.dumps({"ok": True, "result": {}}).encode())

    monkeypatch.setattr(telegram.urllib.request, "urlopen", fake_urlopen)
    bot = TelegramBot("123:SECRET")
    bot.send_message(42, "Hello")
    assert json.loads(requests[0].data) == {"chat_id": 42, "text": "Hello"}
    assert "SECRET" not in repr(bot)


def test_bot_error_does_not_leak_token(monkeypatch):
    def fake_urlopen(request, timeout):
        body = io.BytesIO(json.dumps({"ok": False, "description": "chat not found"}).encode())
        raise urllib.error.HTTPError(request.full_url, 400, "Bad Request", {}, body)

    monkeypatch.setattr(telegram.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(TelegramError) as excinfo:
        TelegramBot("123:SECRET").send_message(42, "Hello")
    assert "chat not found" in str(excinfo.value)
    assert "SECRET" not in str(excinfo.value)


def test_get_updates_sends_telegram_timeout_and_uses_longer_http_timeout(monkeypatch):
    seen = []

    def fake_urlopen(request, timeout):
        seen.append((json.loads(request.data), timeout))
        return FakeResponse(json.dumps({"ok": True, "result": [{"update_id": 7}]}).encode())

    monkeypatch.setattr(telegram.urllib.request, "urlopen", fake_urlopen)
    bot = TelegramBot("123:SECRET")
    assert bot.get_updates(offset=-1, poll_seconds=0) == [{"update_id": 7}]
    assert bot.get_updates(offset=8) == [{"update_id": 7}]
    assert seen[0] == ({"timeout": 0, "allowed_updates": ["message"], "offset": -1}, 10)
    assert seen[1][0]["timeout"] == 25 and seen[1][1] == 35
