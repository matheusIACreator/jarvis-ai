from types import SimpleNamespace

import numpy as np

from jarvis.config import load_config
from jarvis.app import listen_for_command
from jarvis.stt.recorder import RecorderSettings, record_utterance
from jarvis.stt.transcriber import Transcriber
from jarvis.trigger.microphone import BLOCK_SIZE, SAMPLE_RATE

REQUIRED = {"ANTHROPIC_API_KEY": "a", "ELEVENLABS_API_KEY": "e"}


def signal(*parts):
    """Build audio from (seconds, level) parts: quiet noise or a speech-like tone."""
    rng = np.random.default_rng(0)
    chunks = []
    for seconds, level in parts:
        n = int(seconds * SAMPLE_RATE)
        noise = rng.standard_normal(n) * 0.003
        tone = np.sin(2 * np.pi * 220 * np.arange(n) / SAMPLE_RATE) * level
        chunks.append((noise + tone).astype(np.float32))
    return np.concatenate(chunks)


def blocks(audio):
    return [audio[i : i + BLOCK_SIZE] for i in range(0, len(audio), BLOCK_SIZE)]


def test_captures_speech_with_pre_roll_and_stops_on_silence():
    audio = signal((1.0, 0.0), (1.5, 0.2), (2.0, 0.0))
    stream = iter(blocks(audio))
    utterance = record_utterance(stream)
    assert utterance is not None
    seconds = len(utterance) / SAMPLE_RATE
    # 1.5 s of speech + ~0.3 s pre-roll + ~0.8 s trailing silence.
    assert 2.4 < seconds < 2.9
    # Stops early: the rest of the trailing silence is left in the stream.
    assert len(list(stream)) > 0


def test_returns_none_when_nobody_speaks():
    audio = signal((6.0, 0.0))
    assert record_utterance(blocks(audio)) is None


def test_unlimited_listening_captures_command_after_long_silence():
    audio = signal((30.0, 0.0), (1.0, 0.2), (1.0, 0.0))
    utterance = record_utterance(blocks(audio), RecorderSettings(wait_timeout=None))
    assert utterance is not None
    assert 1.7 < len(utterance) / SAMPLE_RATE < 2.3


def test_custom_wait_timeout_still_allows_idle_session_to_end():
    audio = signal((3.0, 0.0), (1.0, 0.2))
    assert record_utterance(blocks(audio), RecorderSettings(wait_timeout=2.0)) is None


def test_unrecognized_noise_does_not_end_listening(monkeypatch):
    import jarvis.app as app

    recordings = iter([np.zeros(16000), np.ones(16000)])
    texts = iter(["  ", "What time is it?"])
    drained = []
    monkeypatch.setattr(app, "record_utterance", lambda mic, settings: next(recordings))
    mic = SimpleNamespace(drain=lambda: drained.append(True))
    transcriber = SimpleNamespace(transcribe=lambda audio: next(texts))
    assert listen_for_command(mic, transcriber, RecorderSettings(wait_timeout=None)) == "What time is it?"
    assert drained == [True]


def test_listen_returns_on_real_timeout_without_transcribing(monkeypatch):
    import jarvis.app as app

    monkeypatch.setattr(app, "record_utterance", lambda mic, settings: None)
    mic = SimpleNamespace(drain=lambda: None)
    assert listen_for_command(mic, object(), RecorderSettings(wait_timeout=5)) == ""


def test_max_duration_caps_long_speech():
    settings = RecorderSettings(max_duration=2.0)
    utterance = record_utterance(blocks(signal((0.5, 0.0), (5.0, 0.2))), settings)
    assert len(utterance) / SAMPLE_RATE < 2.5


def test_short_pauses_do_not_end_the_command():
    audio = signal((0.5, 0.0), (0.6, 0.2), (0.4, 0.0), (0.6, 0.2), (1.5, 0.0))
    utterance = record_utterance(blocks(audio))
    # Both words kept: 0.6 + 0.4 + 0.6 of speech and gap, plus pre-roll and tail.
    assert len(utterance) / SAMPLE_RATE > 2.2


def test_stream_ending_mid_speech_returns_what_was_heard():
    utterance = record_utterance(blocks(signal((0.5, 0.0), (1.0, 0.2))))
    assert utterance is not None


class FakeWhisper:
    def __init__(self):
        self.calls = []

    def transcribe(self, audio, **kwargs):
        self.calls.append(kwargs)
        segments = [SimpleNamespace(text=" What time"), SimpleNamespace(text=" is it? ")]
        return iter(segments), SimpleNamespace(language="en")


def test_transcriber_joins_segments_and_passes_language():
    model = FakeWhisper()
    text = Transcriber(language="en", model=model).transcribe(np.zeros(16000, np.float32))
    assert text == "What time is it?"
    assert model.calls[0]["language"] == "en"
    assert model.calls[0]["vad_filter"] is True
    assert model.calls[0]["beam_size"] == 1


def test_whisper_settings_from_config(tmp_path):
    config = load_config(env_file=None, environ=REQUIRED, root=tmp_path)
    assert (config.whisper_model, config.whisper_language) == ("small", "en")
    config = load_config(
        env_file=None,
        environ={**REQUIRED, "WHISPER_MODEL": "base", "WHISPER_LANGUAGE": "pt"},
        root=tmp_path,
    )
    assert (config.whisper_model, config.whisper_language) == ("base", "pt")
