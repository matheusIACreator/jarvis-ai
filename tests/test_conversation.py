import pytest

import time

from jarvis.conversation import FAREWELL, Conversation, greeting_for, is_dismissal, with_filler


@pytest.mark.parametrize(
    ("hour", "part"),
    [(5, "morning"), (11, "morning"), (12, "afternoon"), (17, "afternoon"), (18, "evening"), (2, "evening")],
)
def test_greeting_follows_time_of_day(hour, part):
    assert greeting_for(hour) == f"Good {part}, sir. How may I help?"


@pytest.mark.parametrize(
    "text",
    ["That's all.", "Thanks, that will be all", "Goodbye!", "No.", "Nothing", "Thank you, that’s all"],
)
def test_dismissals(text):
    assert is_dismissal(text)


@pytest.mark.parametrize(
    "text",
    ["What day is it?", "Nothing is working on my laptop", "Is there anything else on today?", "Say goodbyes"],
)
def test_not_dismissals(text):
    assert not is_dismissal(text)


class Script:
    def __init__(self, *heard):
        self.heard = list(heard)
        self.said = []

    def listen(self):
        return self.heard.pop(0) if self.heard else ""

    def think(self, text):
        return f"answer to {text}"

    def say(self, text):
        self.said.append(text)


def run(script):
    return Conversation(listen=script.listen, think=script.think, say=script.say).run()


def test_answers_follow_ups_until_silence():
    script = Script("What day is it?", "And the time?")
    assert run(script) == 2
    assert script.said == ["answer to What day is it?", "answer to And the time?"]


def test_silence_right_away_ends_quietly():
    script = Script()
    assert run(script) == 0
    assert script.said == []


def test_dismissal_says_farewell_without_thinking():
    script = Script("What day is it?", "Thanks, that's all")
    assert run(script) == 1
    assert script.said[-1] == FAREWELL


def test_finished_hook_ends_session_after_reply():
    script = Script("Thanks, Jarvis", "Should not be heard")
    conversation = Conversation(
        listen=script.listen, think=script.think, say=script.say, finished=lambda: True
    )
    assert conversation.run() == 1
    assert script.heard == ["Should not be heard"]


def test_empty_reply_is_not_spoken():
    script = Script("Hello")
    Conversation(listen=script.listen, think=lambda text: "", say=script.say).run()
    assert script.said == []


def test_filler_plays_only_when_thinking_is_slow():
    events = []

    def slow(text):
        time.sleep(0.15)
        events.append("answer")
        return "slow answer"

    def fast(text):
        return "fast answer"

    def filler():
        events.append("filler")

    assert with_filler(fast, filler, delay=0.1)("q") == "fast answer"
    assert events == []
    assert with_filler(slow, filler, delay=0.05)("q") == "slow answer"
    assert events == ["filler", "answer"]


def test_filler_finishes_before_answer_returns():
    events = []

    def think(text):
        time.sleep(0.1)
        return "answer"

    def filler():
        time.sleep(0.2)
        events.append("filler done")

    assert with_filler(think, filler, delay=0.01)("q") == "answer"
    assert events == ["filler done"]
