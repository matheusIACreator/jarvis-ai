"""Make Jarvis say something with the configured ElevenLabs voice.

Run from the repo root:
    .\\.venv\\Scripts\\python.exe scripts\\say.py "Good evening, sir. All systems are online."
"""

import sys

from jarvis.config import load_config
from jarvis.tts.speaker import Speaker

DEFAULT_TEXT = "Good evening, sir. All systems are online."


def main() -> None:
    config = load_config(required=("ELEVENLABS_API_KEY",))
    speaker = Speaker(config.elevenlabs_api_key, config.elevenlabs_voice_id)
    speaker.speak(" ".join(sys.argv[1:]) or DEFAULT_TEXT)


if __name__ == "__main__":
    main()
