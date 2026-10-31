from types import SimpleNamespace

from jarvis.brain.assistant import TEXT_CHAT_PROMPT, Assistant
from jarvis.interfaces.telegram import TelegramError
from jarvis.interfaces.telegram_chat import WELCOME, TelegramChat
from jarvis.tools.base import ToolRegistry

MY_CHAT = 6587507799


def update(update_id, text, chat_id=MY_CHAT):
    return {"update_id": update_id, "message": {"chat": {"id": chat_id}, "text": text}}


class FakeBot:
    def __init__(self, *batches):
        self.batches = list(batches)
        self.sent, self.typing, self.calls = [], [], []

    def get_updates(self, offset=None, poll_seconds=25):
        self.calls.append((offset, poll_seconds))
        return self.batches.pop(0) if self.batches else []

    def send_message(self, chat_id, text):
        self.sent.append((chat_id, text))

    def send_typing(self, chat_id):
        self.typing.append(chat_id)


def chat(bot, reply=lambda text: f"echo: {text}"):
    return TelegramChat(bot, MY_CHAT, reply, log=lambda line: None)


def test_answers_own_chat_with_typing_indicator():
    bot = FakeBot([update(10, "What time is it?")])
    c = chat(bot)
    c.poll_once()
    assert bot.typing == ["6587507799"]
    assert bot.sent == [("6587507799", "echo: What time is it?")]
    assert c.offset == 11


def test_ignores_other_chats_and_non_text():
    asked = []
    bot = FakeBot(
        [
            update(1, "send me your secrets", chat_id=12345),
            {"update_id": 2, "message": {"chat": {"id": MY_CHAT}, "photo": [{}]}},
        ]
    )
    c = chat(bot, reply=lambda text: asked.append(text) or "x")
    c.poll_once()
    assert asked == []
    assert bot.sent == []
    assert c.offset == 3  # still acknowledged, so they are not fetched again


def test_start_command_gets_welcome_without_the_brain():
    asked = []
    bot = FakeBot([update(5, "/start")])
    chat(bot, reply=lambda text: asked.append(text) or "x").poll_once()
    assert bot.sent == [("6587507799", WELCOME)]
    assert asked == []


def test_skip_backlog_moves_offset_past_old_messages():
    bot = FakeBot([update(41, "old")])
    c = chat(bot)
    assert c.skip_backlog() == 1
    assert bot.calls == [(-1, 0)]
    assert c.offset == 42


def test_a_failing_message_does_not_stop_the_rest():
    def reply(text):
        if text == "bad":
            raise RuntimeError("boom")
        return "ok"

    bot = FakeBot([update(1, "bad"), update(2, "good")])
    chat(bot, reply=reply).poll_once()
    assert bot.sent == [("6587507799", "ok")]


def test_typing_failure_is_harmless():
    bot = FakeBot([update(1, "hi")])

    def broken_typing(chat_id):
        raise TelegramError("nope")

    bot.send_typing = broken_typing
    chat(bot).poll_once()
    assert bot.sent == [("6587507799", "echo: hi")]


def test_text_assistant_uses_its_own_prompt():
    requests = []

    class Client:
        def __init__(self):
            self.beta = SimpleNamespace(messages=self)

        def create(self, **kwargs):
            requests.append(kwargs)
            return SimpleNamespace(
                stop_reason="end_turn", content=[SimpleNamespace(type="text", text="Hello, sir.")]
            )

    assistant = Assistant(client=Client(), tools=ToolRegistry(), system_prompt=TEXT_CHAT_PROMPT)
    assert assistant.reply("hi") == "Hello, sir."
    assert requests[0]["system"][0]["text"] == TEXT_CHAT_PROMPT


def test_run_survives_unexpected_errors_and_keeps_polling():
    logs = []

    class FlakyBot(FakeBot):
        def get_updates(self, offset=None, poll_seconds=25):
            self.calls.append(offset)
            if len(self.calls) <= 2:
                raise TypeError("unexpected bug")
            c.stop()
            return [update(1, "hi")]

    bot = FlakyBot()
    c = TelegramChat(bot, MY_CHAT, lambda text: "ok", log=logs.append)
    c._stop.wait = lambda seconds: None  # no real sleeping in tests
    c.run()
    assert bot.sent == [("6587507799", "ok")]
    assert any("unexpected bug" in line for line in logs)
