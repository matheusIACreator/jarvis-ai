r"""Run only the Telegram chat channel (no microphone or voice). Ctrl+C to stop.

Run from the repo root:  .\.venv\Scripts\python.exe scripts\telegram_chat.py [minutes]
"""

import sys
import time

import anthropic

from jarvis.app import safe_reply
from jarvis.brain.assistant import TEXT_CHAT_PROMPT, Assistant
from jarvis.config import load_config
from jarvis.interfaces.telegram import TelegramBot
from jarvis.interfaces.telegram_chat import TelegramChat
from jarvis.tools.base import ToolRegistry
from jarvis.tools.clock import make_clock_tool


def main() -> None:
    config = load_config(required=("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"))
    assistant = Assistant(
        client=anthropic.Anthropic(api_key=config.anthropic_api_key),
        tools=ToolRegistry([make_clock_tool()]),
        system_prompt=TEXT_CHAT_PROMPT,
    )
    chat = TelegramChat(
        TelegramBot(config.telegram_bot_token),
        config.telegram_chat_id,
        lambda text: safe_reply(assistant, text),
    )
    minutes = float(sys.argv[1]) if len(sys.argv) > 1 else None
    chat.start()
    print("Telegram chat running. Message the bot." + (f" Stops in {minutes:g} min." if minutes else ""))
    deadline = time.time() + minutes * 60 if minutes else None
    while deadline is None or time.time() < deadline:
        time.sleep(1)
    chat.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
