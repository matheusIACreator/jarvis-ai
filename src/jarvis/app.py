"""Jarvis main service: double clap -> startup music -> greeting -> conversation.

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
from jarvis.conversation import FILLER, Conversation, greeting_for, with_filler
from jarvis.stt.recorder import record_utterance
from jarvis.stt.transcriber import Transcriber
from jarvis.tools.base import ToolRegistry
from jarvis.tools.clock import make_clock_tool
from jarvis.tools.session import make_end_conversation_tool
from jarvis.trigger.clap import ClapDetector
from jarvis.trigger.microphone import MicrophoneStream
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
    assistant = Assistant(
        client=anthropic.Anthropic(api_key=config.anthropic_api_key),
        tools=ToolRegistry([make_clock_tool(), make_end_conversation_tool(session_over.set)]),
    )
    transcriber = Transcriber(config.whisper_model, config.whisper_language)
    music = FilePlayer(
        config.startup_audio_path, config.startup_audio_seconds, config.startup_audio_start
    )

    print("Preparing voice clips...")
    filler_clip = speaker.synthesize(FILLER)  # once, so it plays instantly when needed

    print(f"Loading Whisper '{config.whisper_model}'...")
    _ = transcriber.model  # load now so the first command is not slow
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
        )
        with ThreadPoolExecutor(max_workers=1) as pool:
            while True:
                print("Waiting for a double clap... (Ctrl+C to stop)")
                detector = ClapDetector()
                for block in mic:
                    if detector.process(block):
                        break
                session_over.clear()
                try:
                    wake_up(music, speaker, pool)
                    conversation.run()
                except Exception as exc:  # keep the service alive after a failed session
                    print(f"(Session error: {type(exc).__name__}: {exc})")
                mic.drain()


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
