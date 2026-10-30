"""Load Jarvis configuration from the environment and an optional `.env` file.

Values already set in the real environment win over values from `.env`.
The `.env` file is read but never written to `os.environ`.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_STARTUP_AUDIO = Path("assets") / "audio" / "startup.mp3"

REQUIRED_KEYS = ("ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY")

# ElevenLabs "Daniel": British male, formal broadcaster tone.
DEFAULT_VOICE_ID = "onwK4e9ZLuTAKqWW03F9"

# Values copied unchanged from .env.example start with this prefix.
PLACEHOLDER_PREFIX = "your-"


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str | None
    elevenlabs_api_key: str | None
    elevenlabs_voice_id: str
    startup_audio_path: Path
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    def __repr__(self) -> str:
        # Never print secrets, e.g. in tracebacks or logs.
        return (
            f"Config(elevenlabs_voice_id={self.elevenlabs_voice_id!r}, "
            f"startup_audio_path={self.startup_audio_path!r}, "
            f"telegram_enabled={self.telegram_enabled})"
        )

    @property
    def telegram_enabled(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)


def parse_env(text: str) -> dict[str, str]:
    """Parse `.env` content: `KEY=value` lines, `#` comments, optional quotes and `export`."""
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value or value.startswith(PLACEHOLDER_PREFIX):
        return None
    return value


def _resolve_path(value: str | None, default: Path, root: Path) -> Path:
    path = Path(value) if value else default
    return path if path.is_absolute() else root / path


def load_config(
    env_file: Path | None = DEFAULT_ENV_FILE,
    environ: Mapping[str, str] | None = None,
    root: Path = PROJECT_ROOT,
    required: tuple[str, ...] = REQUIRED_KEYS,
) -> Config:
    """Build a `Config`, raising `ConfigError` that names every missing required key.

    Pass a smaller `required` tuple for tools that only use part of the configuration.
    """
    merged: dict[str, str] = {}
    if env_file is not None and env_file.is_file():
        merged.update(parse_env(env_file.read_text(encoding="utf-8-sig")))
    merged.update(os.environ if environ is None else environ)

    values = {key: _clean(merged.get(key)) for key in merged}
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise ConfigError(
            "Missing required configuration: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in real values."
        )

    return Config(
        anthropic_api_key=values.get("ANTHROPIC_API_KEY"),
        elevenlabs_api_key=values.get("ELEVENLABS_API_KEY"),
        elevenlabs_voice_id=values.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID,
        startup_audio_path=_resolve_path(
            values.get("STARTUP_AUDIO_PATH"), DEFAULT_STARTUP_AUDIO, root
        ),
        telegram_bot_token=values.get("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=values.get("TELEGRAM_CHAT_ID"),
    )
