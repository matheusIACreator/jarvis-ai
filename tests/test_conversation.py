import pytest

from jarvis.conversation import FAREWELL, Conversation, greeting_for, is_dismissal


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
