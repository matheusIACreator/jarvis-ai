"""Jarvis main service: double clap or "Hey Jarvis" -> startup music -> greeting -> conversation.

Run with:  .\\.venv\\Scripts\\python.exe -m jarvis
Ctrl+C to stop.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from datetime import datetime

import anthropic

from jarvis.background import BackgroundTasks
from jarvis.brain.assistant import BACKGROUND_PROMPT, FALLBACK_REPLY, TEXT_CHAT_PROMPT, Assistant
from jarvis.config import ConfigError, load_config, PROJECT_ROOT
from jarvis.memory import Memory
from jarvis.interfaces.dashboard import Dashboard
from jarvis.confirmation import ConfirmationGate
from jarvis.conversation import FILLER, Conversation, greeting_for, with_filler
from jarvis.interfaces.telegram import TelegramBot
from jarvis.interfaces.telegram_chat import TelegramChat
from jarvis.stt.recorder import RecorderSettings, record_utterance
from jarvis.stt.transcriber import Transcriber
from jarvis.tools.base import ToolRegistry
from jarvis.tools.background import make_background_tool
from jarvis.tools.clock import make_clock_tool
from jarvis.tools.session import make_end_conversation_tool
from jarvis.tools.telegram import make_telegram_tool
from jarvis.trigger.clap import ClapDetector, ClapSettings
from jarvis.trigger.microphone import MicrophoneStream
from jarvis.trigger.wake_word import WakeWordDetector
from jarvis.tts.audio_file import FilePlayer
from jarvis.tts.speaker import Speaker

TROUBLE_CONNECTING = "I'm afraid I can't reach my servers right now, sir."
TROUBLE_GENERIC = "Something went wrong on my end, sir."


def main() -> None:
    try:
        config = load_config()
    except ConfigError as exc:
        raise SystemExit(str(exc)) from None

    speaker = Speaker(config.elevenlabs_api_key, config.elevenlabs_voice_id)
    session_over = threading.Event()
    gate = ConfirmationGate()
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    memory = Memory(PROJECT_ROOT / "vault")
    tools = [make_clock_tool(), make_end_conversation_tool(session_over.set), memory.tool()]
    telegram_chat = None
    background_tasks = None
    if config.telegram_enabled:
        bot = TelegramBot(config.telegram_bot_token)
        chat_id = config.telegram_chat_id
        tools.append(make_telegram_tool(gate, lambda text: bot.send_message(chat_id, text)))
        background_tasks = make_background_tasks(client, lambda text: bot.send_message(chat_id, text))
        tools.append(make_background_tool(gate, background_tasks))
        # Text chat gets its own conversation, separate from voice sessions.
        text_assistant = Assistant(
            client=client, tools=ToolRegistry([make_clock_tool(), memory.tool()]), system_prompt=TEXT_CHAT_PROMPT,
            memory_sink=lambda user, reply: memory.save(user, reply, "telegram")
        )
        telegram_chat = TelegramChat(bot, chat_id, lambda text: safe_reply(text_assistant, text))
    else:
        print("Telegram not configured (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID); messaging is off.")
    assistant = Assistant(client=client, tools=ToolRegistry(tools),
                          memory_sink=lambda user, reply: memory.save(user, reply, "voz"))
    web_assistant = Assistant(
        client=client, tools=ToolRegistry([make_clock_tool(), memory.tool()]),
        system_prompt=TEXT_CHAT_PROMPT.replace("in a Telegram chat", "in a local web dashboard"),
        memory_sink=lambda user, reply: memory.save(user, reply, "web"),
    )
    dashboard = Dashboard(memory, lambda text: safe_reply(web_assistant, text))
    transcriber = Transcriber(config.whisper_model, config.whisper_language)
    music = FilePlayer(
        config.startup_audio_path, config.startup_audio_seconds, config.startup_audio_start
    )

    print("Preparing voice clips...")
    filler_clip = speaker.synthesize(FILLER)  # once, so it plays instantly when needed

    print(f"Loading Whisper '{config.whisper_model}'...")
    _ = transcriber.model  # load now so the first command is not slow
    wake_word = None
    if config.wake_word_threshold:
        print("Loading wake word 'Hey Jarvis'...")
        wake_word = WakeWordDetector(config.wake_word_threshold)
        _ = wake_word.model
    if not music.load():
        print(f"No startup music at {config.startup_audio_path}; Jarvis will just greet.")

    def think(text: str) -> str:
        dashboard.phase("thinking")
        return safe_reply(assistant, text)

    def confirm(text: str) -> str | None:
        resolution = gate.resolve(text)
        if resolution is None:
            return None
        # Tell the model what really happened, or it may doubt a "Sent" it never saw happen.
        assistant.remember(text, resolution.reply, resolution.record)
        return resolution.reply

    def say(text: str) -> None:
        print(f"jarvis> {text}")
        dashboard.message("assistant", text)
        dashboard.phase("speaking")
        try:
            speaker.speak(text)
        finally:
            dashboard.phase("listening")

    with ExitStack() as services:
        dashboard.start()
        services.callback(dashboard.stop)
        if background_tasks:
            services.callback(background_tasks.stop)
        if telegram_chat:
            services.callback(telegram_chat.stop)
            telegram_chat.start()
            print("Telegram chat is on: message the bot to talk to Jarvis.")
        mic = services.enter_context(MicrophoneStream())

        def listen() -> str:
            dashboard.phase("listening")
            return listen_for_command(
                mic, transcriber, RecorderSettings(wait_timeout=config.session_idle_seconds)
            )

        conversation = Conversation(
            listen=listen,
            think=with_filler(think, lambda: speaker.play(filler_clip)),
            say=say,
            on_heard=lambda text: (print(f"you> {text}"), dashboard.message("user", text)),
            finished=session_over.is_set,
            confirm=confirm,
        )
        with ThreadPoolExecutor(max_workers=1) as pool:
            while True:
                print(
                    "Waiting for a double clap"
                    + (' or "Hey Jarvis"' if wake_word else "")
                    + "... (Ctrl+C to stop)"
                )
                dashboard.phase("idle")
                clap = ClapDetector(ClapSettings(min_peak=config.clap_min_peak))
                wait_for_trigger(mic, clap, wake_word)
                session_over.clear()
                gate.cancel()  # nothing carries over from a previous session
                try:
                    dashboard.phase("speaking")
                    wake_up(music, speaker, pool)
                    conversation.run()
                except Exception as exc:  # keep the service alive after a failed session
                    print(f"(Session error: {type(exc).__name__}: {exc})")
                finally:
                    gate.cancel()  # silence, dismissal or an error invalidates unconfirmed work
                mic.drain()


def listen_for_command(mic, transcriber: Transcriber, settings: RecorderSettings) -> str:
    """Keep listening after noise/unrecognized speech; only an actual timeout ends the turn."""
    mic.drain()  # drop what the mic heard while Jarvis was talking
    while True:
        audio = record_utterance(mic, settings)
        if audio is None:
            return ""
        text = transcriber.transcribe(audio).strip()
        if text:
            return text


def make_background_tasks(client: anthropic.Anthropic, send: Callable[[str], None]) -> BackgroundTasks:
    """Give each job fresh history and read-only tools, separate from both chat channels."""
    def work(task: str) -> str:
        worker = Assistant(
            client=client, tools=ToolRegistry([make_clock_tool()]), system_prompt=BACKGROUND_PROMPT
        )
        result = worker.reply(task)
        if result == FALLBACK_REPLY:
            raise RuntimeError("The background assistant could not complete the task.")
        return result

    return BackgroundTasks(work, send)


def safe_reply(assistant: Assistant, text: str) -> str:
    """Ask the brain, turning API failures into a short apology instead of an exception."""
    try:
        return assistant.reply(text)
    except anthropic.APIConnectionError:
        return TROUBLE_CONNECTING
    except anthropic.APIError as exc:
        print(f"(Anthropic API error: {exc})")
        return TROUBLE_GENERIC


def wait_for_trigger(mic, clap: ClapDetector, wake_word: WakeWordDetector | None) -> str:
    """Block until a double clap or the wake word. Returns which one fired."""
    if wake_word:
        wake_word.reset()
    for block in mic:
        if clap.process(block):
            print("(double clap)")
            return "clap"
        if wake_word and wake_word.process(block):
            print('("Hey Jarvis")')
            return "wake word"
    return "stopped"


def wake_up(music: FilePlayer, speaker: Speaker, pool: ThreadPoolExecutor) -> None:
    """Play the startup music while the greeting is generated, then speak it."""
    greeting = greeting_for(datetime.now().hour)
    pending = pool.submit(speaker.synthesize, greeting)
    if music.start():
        music.wait()
    print(f"jarvis> {greeting}")
    speaker.play(pending.result())


def run() -> None:
    try:
        main()
    except KeyboardInterrupt:
        print("\nJarvis stopped.")
