"""Local speech-to-text with faster-whisper.

The model loads on first use (and is downloaded once into the Hugging Face cache), so
importing this module stays cheap.
"""

from __future__ import annotations

import os

import numpy as np

DEFAULT_MODEL = "small"
DEFAULT_LANGUAGE = "en"


class Transcriber:
    def __init__(
        self,
        model_size: str = DEFAULT_MODEL,
        language: str | None = DEFAULT_LANGUAGE,
        model=None,
    ) -> None:
        self.model_size = model_size
        self.language = language
        self._model = model

    @property
    def model(self):
        if self._model is None:
            # Windows without Developer Mode has no symlinks; the cache still works, just bigger.
            os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
            from faster_whisper import WhisperModel

            # int8 on CPU: the laptop has no CUDA GPU to rely on.
            self._model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        return self._model

    def transcribe(self, audio: np.ndarray) -> str:
        """Return the text of 16 kHz mono float32 `audio`, or "" if nothing was said."""
        segments, _info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=1,  # greedy: same text as beam 5 on short commands, ~0.3 s faster
            vad_filter=True,  # drops leading/trailing noise that Whisper may hallucinate on
            condition_on_previous_text=False,
        )
        return " ".join(segment.text.strip() for segment in segments).strip()
