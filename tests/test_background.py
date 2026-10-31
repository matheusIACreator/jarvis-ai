import threading
from types import SimpleNamespace

import pytest

from jarvis.app import make_background_tasks
from jarvis.background import BUSY, FAILED, MESSAGE_CHARS, BackgroundTasks
from jarvis.brain.assistant import BACKGROUND_PROMPT, FALLBACK_REPLY
from jarvis.confirmation import ConfirmationGate
from jarvis.conversation import Conversation, FAREWELL
from jarvis.tools.background import STARTED, make_background_tool
from jarvis.tools.base import ToolRegistry


def request(gate, tasks, task="Plan a week of study"):
    return ToolRegistry([make_background_tool(gate, tasks)]).run(
        "start_background_task", {"task": task}
    )


def test_conversation_confirms_then_returns_while_task_keeps_running():
    entered, release = threading.Event(), threading.Event()
    sent, said = [], []

    def work(task):
        entered.set()
        assert release.wait(3)
        return "Study Python on Monday."

    tasks = BackgroundTasks(work, sent.append)
    gate = ConfirmationGate()
    heard = iter(["Plan my week and notify me", "yes", "that's all", ""])

    def think(text):
        result = request(gate, tasks)
        assert not result.is_error
        assert "Shall I start" in result.content
        assert not entered.is_set()
        assert sent == []
        return "Shall I start the study plan and send the result to Telegram?"

    try:
        Conversation(
            listen=lambda: next(heard), think=think, say=said.append,
            confirm=lambda text: (r := gate.resolve(text)) and r.reply,
        ).run()
        assert entered.wait(1)
        assert tasks.busy
        assert said[-2:] == [STARTED, FAREWELL]
        gate.cancel()  # ending a voice session must not cancel already confirmed work
        assert sent == []
    finally:
        release.set()
        assert tasks.wait(3)
    assert len(sent) == 1
    assert "Study Python on Monday." in sent[0]


@pytest.mark.parametrize("answer", ["no", "yes but change it", None])
def test_unconfirmed_task_never_runs_or_notifies(answer):
    ran, sent = [], []
    tasks = BackgroundTasks(lambda task: ran.append(task) or "result", sent.append)
    gate = ConfirmationGate()
    request(gate, tasks)
    if answer is None:
        gate.cancel()
    else:
        gate.resolve(answer)
    assert gate.resolve("yes") is None
    assert ran == sent == []


def test_rejects_overlap_without_replacing_pending_confirmation():
    release = threading.Event()
    tasks = BackgroundTasks(lambda task: release.wait(3) and "done", lambda text: None)
    gate = ConfirmationGate()
    try:
        tasks.start("first")
        result = request(gate, tasks, "second")
        assert result.is_error and BUSY in result.content
        assert gate.pending is None
        with pytest.raises(ValueError, match="already running"):
            tasks.start("third")
    finally:
        release.set()
        assert tasks.wait(3)


def test_long_results_are_delivered_in_order_without_truncation():
    sent = []
    result = "á😀" * 3000
    tasks = BackgroundTasks(lambda task: result, sent.append)
    tasks.start("test")
    assert tasks.wait(3)
    assert "".join(sent) == f"Background task finished.\n\nTask: test\n\n{result}"
    assert all(len(part) <= MESSAGE_CHARS for part in sent)
    assert all(len(part.encode("utf-16-le")) // 2 <= 4096 for part in sent)


@pytest.mark.parametrize("empty", [False, True])
def test_worker_failure_notifies_without_exposing_exception_text(empty):
    sent, logs = [], []

    def work(task):
        if empty:
            return " "
        raise RuntimeError("secret request contents")

    tasks = BackgroundTasks(work, sent.append, logs.append)
    tasks.start("test")
    assert tasks.wait(3)
    assert FAILED in sent[0]
    assert "secret" not in "".join(sent + logs)
    assert not tasks.busy


def test_delivery_failure_is_logged_without_retry_and_next_task_can_start():
    sent, logs = [], []

    def notify(text):
        sent.append(text)
        raise RuntimeError("secret bot URL")

    tasks = BackgroundTasks(lambda task: "done", notify, logs.append)
    for task in ["first", "second"]:
        tasks.start(task)
        assert tasks.wait(3)
    assert len(sent) == 2
    assert all("not retried" in line for line in logs)
    assert "secret" not in "".join(logs)


def test_shutdown_suppresses_notification_and_rejects_new_work():
    entered, release = threading.Event(), threading.Event()
    sent = []

    def work(task):
        entered.set()
        assert release.wait(3)
        return "done"

    tasks = BackgroundTasks(work, sent.append)
    try:
        tasks.start("test")
        assert entered.wait(1)
        tasks.stop()
        with pytest.raises(RuntimeError, match="stopped"):
            tasks.start("another")
    finally:
        release.set()
        assert tasks.wait(3)
    assert sent == []


def test_empty_task_is_rejected_before_confirmation():
    tasks = BackgroundTasks(lambda task: "done", lambda text: None)
    gate = ConfirmationGate()
    assert request(gate, tasks, "  ").is_error
    assert gate.pending is None
    with pytest.raises(ValueError, match="empty"):
        tasks.start(" ")


def test_application_worker_has_fresh_history_and_only_read_only_tools():
    requests, sent = [], []

    class Client:
        def __init__(self):
            self.beta = SimpleNamespace(messages=self)

        def create(self, **kwargs):
            requests.append(kwargs)
            return SimpleNamespace(
                stop_reason="end_turn", content=[SimpleNamespace(type="text", text="A plan.")]
            )

    tasks = make_background_tasks(Client(), sent.append)
    for task in ["First plan", "Second plan"]:
        tasks.start(task)
        assert tasks.wait(3)
    assert len(sent) == 2
    for index, task in enumerate(["First plan", "Second plan"]):
        assert requests[index]["messages"] == [{"role": "user", "content": task}]
        assert requests[index]["system"][0]["text"] == BACKGROUND_PROMPT
        assert {tool["name"] for tool in requests[index]["tools"]} == {
            "get_current_datetime", "advisor"
        }


def test_application_reports_incomplete_analysis_as_failure():
    class Client:
        def __init__(self):
            self.beta = SimpleNamespace(messages=self)

        def create(self, **kwargs):
            return SimpleNamespace(stop_reason="refusal", content=[])

    sent = []
    tasks = make_background_tasks(Client(), sent.append)
    tasks.start("test")
    assert tasks.wait(3)
    assert FAILED in sent[0]
    assert FALLBACK_REPLY not in sent[0]
