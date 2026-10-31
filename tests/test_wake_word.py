import numpy as np

from jarvis.app import wait_for_trigger
from jarvis.config import load_config
from jarvis.trigger.wake_word import FRAME, MODEL_NAME, WakeWordDetector

REQUIRED = {"ANTHROPIC_API_KEY": "a", "ELEVENLABS_API_KEY": "e"}


class FakeModel:
    """Scores 0.9 on the frame numbers in `hits`, 0 otherwise."""

    def __init__(self, hits=()):
        self.hits = set(hits)
        self.frames = []
        self.resets = 0

    def predict(self, frame):
        self.frames.append(frame)
        score = 0.9 if len(self.frames) in self.hits else 0.0
        return {MODEL_NAME: score}

    def reset(self):
        self.resets += 1


def test_blocks_are_regrouped_into_whole_int16_frames():
    model = FakeModel()
    detector = WakeWordDetector(model=model)
    for _ in range(5):
        detector.process(np.full(512, 0.5, np.float32))  # 2560 samples = 2 frames
    assert len(model.frames) == 2
    assert all(len(f) == FRAME and f.dtype == np.int16 for f in model.frames)
    assert model.frames[0][0] == int(0.5 * 32767)


def test_fires_on_high_score_and_resets():
    model = FakeModel(hits={3})
    detector = WakeWordDetector(threshold=0.5, model=model)
    results = [detector.process(np.zeros(FRAME, np.float32)) for _ in range(4)]
    assert results == [False, False, True, False]
    assert model.resets == 1


def test_threshold_is_respected():
    detector = WakeWordDetector(threshold=0.95, model=FakeModel(hits={1}))
    assert not detector.process(np.zeros(FRAME, np.float32))


class FakeDetector:
    def __init__(self, fire_at):
        self.fire_at, self.count = fire_at, 0

    def process(self, block):
        self.count += 1
        return self.count == self.fire_at

    def reset(self):
        pass


def test_wait_for_trigger_returns_first_source():
    blocks = [np.zeros(4, np.float32)] * 10
    assert wait_for_trigger(iter(blocks), FakeDetector(3), FakeDetector(5)) == "clap"
    assert wait_for_trigger(iter(blocks), FakeDetector(9), FakeDetector(2)) == "wake word"
    assert wait_for_trigger(iter(blocks), FakeDetector(4), None) == "clap"


def test_wake_word_threshold_setting(tmp_path):
    def threshold(value):
        environ = {**REQUIRED, "WAKE_WORD_THRESHOLD": value}
        return load_config(env_file=None, environ=environ, root=tmp_path).wake_word_threshold

    assert threshold("") == 0.5
    assert threshold("0.7") == 0.7
    assert threshold("0") is None
