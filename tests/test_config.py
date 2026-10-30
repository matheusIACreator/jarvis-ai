from pathlib import Path

import pytest

from jarvis.config import ConfigError, load_config, parse_env

REQUIRED = {
    "ANTHROPIC_API_KEY": "sk-ant-test",
    "ELEVENLABS_API_KEY": "el-test",
    "ELEVENLABS_VOICE_ID": "voice-1",
}


def test_parse_env_handles_comments_quotes_and_export():
    text = """
# a comment
ANTHROPIC_API_KEY=abc
export ELEVENLABS_VOICE_ID = "voice 1"
SINGLE='x # not a comment'
INLINE=value # trailing comment
EMPTY=
not a pair
"""
    assert parse_env(text) == {
        "ANTHROPIC_API_KEY": "abc",
        "ELEVENLABS_VOICE_ID": "voice 1",
        "SINGLE": "x # not a comment",
        "INLINE": "value",
        "EMPTY": "",
    }


def test_load_from_environ_only(tmp_path):
    config = load_config(env_file=None, environ=REQUIRED, root=tmp_path)
    assert config.anthropic_api_key == "sk-ant-test"
    assert config.startup_audio_path == tmp_path / "assets" / "audio" / "startup.mp3"
    assert not config.telegram_enabled


def test_env_file_is_read_and_environ_wins(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "ANTHROPIC_API_KEY=from-file\n"
        "ELEVENLABS_API_KEY=el-file\n"
        "ELEVENLABS_VOICE_ID=voice-file\n"
        "STARTUP_AUDIO_PATH=sounds/intro.mp3\n",
        encoding="utf-8",
    )
    config = load_config(
        env_file=env_file, environ={"ANTHROPIC_API_KEY": "from-env"}, root=tmp_path
    )
    assert config.anthropic_api_key == "from-env"
    assert config.elevenlabs_voice_id == "voice-file"
    assert config.startup_audio_path == tmp_path / "sounds" / "intro.mp3"


def test_missing_env_file_is_not_an_error(tmp_path):
    config = load_config(env_file=tmp_path / "nope.env", environ=REQUIRED, root=tmp_path)
    assert config.elevenlabs_api_key == "el-test"


def test_missing_keys_are_all_reported(tmp_path):
    with pytest.raises(ConfigError) as excinfo:
        load_config(env_file=None, environ={"ELEVENLABS_API_KEY": "x"}, root=tmp_path)
    message = str(excinfo.value)
    assert "ANTHROPIC_API_KEY" in message
    assert "ELEVENLABS_VOICE_ID" in message
    assert "ELEVENLABS_API_KEY" not in message


def test_placeholders_from_example_count_as_missing(tmp_path):
    example = Path(__file__).resolve().parents[1] / ".env.example"
    with pytest.raises(ConfigError, match="ANTHROPIC_API_KEY"):
        load_config(env_file=example, environ={}, root=tmp_path)


def test_absolute_audio_path_is_kept(tmp_path):
    audio = tmp_path / "elsewhere" / "music.mp3"
    config = load_config(
        env_file=None,
        environ={**REQUIRED, "STARTUP_AUDIO_PATH": str(audio)},
        root=tmp_path / "root",
    )
    assert config.startup_audio_path == audio


def test_telegram_enabled_needs_token_and_chat(tmp_path):
    config = load_config(
        env_file=None,
        environ={**REQUIRED, "TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "42"},
        root=tmp_path,
    )
    assert config.telegram_enabled


def test_repr_hides_secrets(tmp_path):
    config = load_config(env_file=None, environ=REQUIRED, root=tmp_path)
    assert "sk-ant-test" not in repr(config)
    assert "el-test" not in repr(config)
