import numpy as np

from jarvis.config import load_config
from jarvis.trigger.microphone import MicrophoneStream
from jarvis.tts.audio_file import FilePlayer, skip_start, trim_with_fade
from jarvis.tts.speaker import Speaker

REQUIRED = {"ANTHROPIC_API_KEY": "a", "ELEVENLABS_API_KEY": "e"}


def test_trim_cuts_and_fades_out():
    audio = np.ones((1000, 2), np.float32)
    trimmed = trim_with_fade(audio, sample_rate=100, max_seconds=5, fade_seconds=1)
    assert trimmed.shape == (500, 2)
    assert trimmed[0, 0] == 1.0
    assert trimmed[-1, 0] == 0.0
    assert 0.0 < trimmed[450, 1] < 1.0
    assert audio[-1, 0] == 1.0  # input untouched


def test_short_audio_and_no_limit_are_unchanged():
    audio = np.ones((300, 2), np.float32)
    assert trim_with_fade(audio, 100, max_seconds=5) is audio
    assert trim_with_fade(audio, 100, max_seconds=None) is audio


def test_skip_start_drops_seconds_and_fades_in():
    audio = np.ones((1000, 2), np.float32)
    skipped = skip_start(audio, sample_rate=100, start_seconds=6, fade_in=0.5)
    assert skipped.shape == (400, 2)
    assert skipped[0, 0] == 0.0
    assert skipped[-1, 0] == 1.0
    assert skip_start(audio, 100, 0) is audio


def test_missing_file_does_not_play(tmp_path):
    player = FilePlayer(tmp_path / "missing.mp3")
    assert not player.load()
    assert not player.start()


def test_microphone_drain_empties_queue():
    mic = MicrophoneStream()
    for _ in range(3):
        mic._callback(np.zeros((4, 1), np.float32), 4, None, 0)
    assert mic.drain() == 3
    assert mic.drain() == 0


def test_startup_seconds_setting(tmp_path):
    def seconds(value):
        environ = {**REQUIRED, "STARTUP_AUDIO_SECONDS": value}
        return load_config(env_file=None, environ=environ, root=tmp_path).startup_audio_seconds

    assert seconds("") == 10.0
    assert seconds("4.5") == 4.5
    assert seconds("0") is None


def test_startup_start_setting(tmp_path):
    def start(value):
        environ = {**REQUIRED, "STARTUP_AUDIO_START": value}
        return load_config(env_file=None, environ=environ, root=tmp_path).startup_audio_start

    assert start("") == 0.0
    assert start("6") == 6.0
    assert start("-2") == 0.0


class FakeTextToSpeech:
    def stream(self, voice_id, **kwargs):
        return iter([b"\x01", b"\x02\x03", b"\x04"])


def test_synthesize_returns_whole_frames():
    client = type("Client", (), {"text_to_speech": FakeTextToSpeech()})()
    speaker = Speaker(api_key="unused", voice_id="v", client=client)
    assert speaker.synthesize("Hi") == b"\x01\x02\x03\x04"


def test_clap_min_peak_setting(tmp_path):
    def peak(value):
        environ = {**REQUIRED, "CLAP_MIN_PEAK": value}
        return load_config(env_file=None, environ=environ, root=tmp_path).clap_min_peak

    assert peak("") == 0.08
    assert peak("0.15") == 0.15
