"""Spoken wake-up ("Hey Jarvis") with openWakeWord, as a fallback to the double clap.

openWakeWord scores 80 ms frames of 16 kHz int16 audio. Microphone blocks are a different
size, so samples are buffered into whole frames. The pretrained "hey_jarvis" model is
downloaded once on first use (a few MB).
"""

from __future__ import annotations

import numpy as np

MODEL_NAME = "hey_jarvis"
FRAME = 1280  # samples per openWakeWord frame (80 ms at 16 kHz)
DEFAULT_THRESHOLD = 0.5


def load_model():
    from openwakeword import utils
    from openwakeword.model import Model

    try:
        return Model(wakeword_models=[MODEL_NAME], inference_framework="onnx")
    except Exception:
        # Models are not bundled with the package; fetch them once, then retry.
        utils.download_models(model_names=[MODEL_NAME])
        return Model(wakeword_models=[MODEL_NAME], inference_framework="onnx")


class WakeWordDetector:
    def __init__(self, threshold: float = DEFAULT_THRESHOLD, model=None) -> None:
        self.threshold = threshold
        self._model = model
        self._pending = np.zeros(0, np.int16)
        self.last_score = 0.0

    @property
    def model(self):
        if self._model is None:
            self._model = load_model()
        return self._model

    def process(self, block: np.ndarray) -> bool:
        """Feed one mono float32 block. Returns True when "Hey Jarvis" is heard."""
        samples = (np.clip(block, -1.0, 1.0) * 32767).astype(np.int16)
        self._pending = np.concatenate([self._pending, samples])
        heard = False
        while len(self._pending) >= FRAME:
            frame, self._pending = self._pending[:FRAME], self._pending[FRAME:]
            self.last_score = float(self.model.predict(frame)[MODEL_NAME])
            if self.last_score >= self.threshold:
                heard = True
        if heard:
            self.reset()
        return heard

    def reset(self) -> None:
        """Forget buffered audio so one utterance cannot trigger twice."""
        self._pending = np.zeros(0, np.int16)
        self.model.reset()
