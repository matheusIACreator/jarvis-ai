"""Talk to Jarvis's brain by typing. Add --speak to hear the replies.

Run from the repo root:
    .\\.venv\\Scripts\\python.exe scripts\\chat.py
    .\\.venv\\Scripts\\python.exe scripts\\chat.py --speak
Empty line or Ctrl+C to quit.
"""

import sys

import anthropic

from jarvis.brain.assistant import Assistant
from jarvis.config import load_config
from jarvis.tools.base import ToolRegistry
from jarvis.tools.clock import make_clock_tool
from jarvis.tts.speaker import Speaker


def main() -> None:
    speak = "--speak" in sys.argv[1:]
    config = load_config(
        required=("ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY") if speak else ("ANTHROPIC_API_KEY",)
    )
    assistant = Assistant(
        client=anthropic.Anthropic(api_key=config.anthropic_api_key),
        tools=ToolRegistry([make_clock_tool()]),
    )
    speaker = Speaker(config.elevenlabs_api_key, config.elevenlabs_voice_id) if speak else None

    while True:
        user_text = input("you> ").strip()
        if not user_text:
            break
        try:
            reply = assistant.reply(user_text)
        except anthropic.APIConnectionError:
            print("jarvis> (no connection to the Anthropic API)")
            continue
        except anthropic.APIStatusError as exc:
            print(f"jarvis> (API error {exc.status_code}: {exc.message})")
            continue
        print(f"jarvis> {reply}")
        if speaker:
            speaker.speak(reply)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
