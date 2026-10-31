"""Jarvis main service: double clap or "Hey Jarvis" -> startup music -> greeting -> conversation.

Run with:  .\\.venv\\Scripts\\python.exe -m jarvis
Ctrl+C to stop.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import anthropic

from jarvis.brain.assistant import Assistant
from jarvis.config import ConfigError, load_config
from jarvis.confirmation import ConfirmationGate
from jarvis.conversation import FILLER, Conversation, greeting_for, with_filler
from jarvis.interfaces.telegram import TelegramBot
from jarvis.stt.recorder import record_utterance
from jarvis.stt.transcriber import Transcriber
from jarvis.tools.base import ToolRegistry
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
    tools = [make_clock_tool(), make_end_conversation_tool(session_over.set)]
    if config.telegram_enabled:
        bot = TelegramBot(config.telegram_bot_token)
        chat_id = config.telegram_chat_id
        tools.append(make_telegram_tool(gate, lambda text: bot.send_message(chat_id, text)))
    else:
        print("Telegram not configured (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID); messaging is off.")
    assistant = Assistant(
        client=anthropic.Anthropic(api_key=config.anthropic_api_key),
        tools=ToolRegistry(tools),
    )
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
        try:
            return assistant.reply(text)
        except anthropic.APIConnectionError:
            return TROUBLE_CONNECTING
        except anthropic.APIError as exc:
            print(f"(Anthropic API error: {exc})")
            return TROUBLE_GENERIC

    def confirm(text: str) -> str | None:
        resolution = gate.resolve(text)
        if resolution is None:
            return None
        # Tell the model what really happened, or it may doubt a "Sent" it never saw happen.
        assistant.remember(text, resolution.reply, resolution.record)
        return resolution.reply

    def say(text: str) -> None:
        print(f"jarvis> {text}")
        speaker.speak(text)

    with MicrophoneStream() as mic:

        def listen() -> str:
            mic.drain()  # drop what the mic heard while Jarvis was talking
            audio = record_utterance(mic)
            return transcriber.transcribe(audio) if audio is not None else ""

        conversation = Conversation(
            listen=listen,
            think=with_filler(think, lambda: speaker.play(filler_clip)),
            say=say,
            on_heard=lambda text: print(f"you> {text}"),
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
                clap = ClapDetector(ClapSettings(min_peak=config.clap_min_peak))
                wait_for_trigger(mic, clap, wake_word)
                session_over.clear()
                gate.cancel()  # nothing carries over from a previous session
                try:
                    wake_up(music, speaker, pool)
                    conversation.run()
                except Exception as exc:  # keep the service alive after a failed session
                    print(f"(Session error: {type(exc).__name__}: {exc})")
                mic.drain()


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
