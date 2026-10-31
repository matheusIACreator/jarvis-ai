"""Record one spoken command from the microphone and print what Whisper heard.

Run from the repo root:  .\\.venv\\Scripts\\python.exe scripts\\listen.py
Start talking within 5 seconds; it stops after a short pause.
"""

import time

from jarvis.config import load_config
from jarvis.stt.recorder import record_utterance
from jarvis.stt.transcriber import Transcriber
from jarvis.trigger.microphone import SAMPLE_RATE, MicrophoneStream


def main() -> None:
    config = load_config(required=())
    transcriber = Transcriber(config.whisper_model, config.whisper_language)
    print(f"Loading Whisper '{config.whisper_model}'...")
    _ = transcriber.model

    with MicrophoneStream() as mic:
        print("Listening. Say something.")
        audio = record_utterance(mic)
    if audio is None:
        print("No speech heard.")
        return

    start = time.perf_counter()
    text = transcriber.transcribe(audio)
    elapsed = time.perf_counter() - start
    print(f"Heard ({len(audio) / SAMPLE_RATE:.1f} s audio, {elapsed:.1f} s to transcribe): {text!r}")


if __name__ == "__main__":
    main()
