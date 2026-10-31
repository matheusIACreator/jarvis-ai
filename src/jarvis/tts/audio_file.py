"""Play a local audio file (the startup music), decoded with PyAV.

PyAV comes with faster-whisper and reads mp3, wav, ogg and more, so no extra library is
needed. Playback is non-blocking: start it, do other work (like preparing the greeting),
then wait for it.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

PLAYBACK_RATE = 44_100
CHANNELS = 2


def decode(path: Path, sample_rate: int = PLAYBACK_RATE) -> np.ndarray:
    """Decode `path` to float32 stereo frames, shape (frames, 2), at `sample_rate`."""
    import av

    with av.open(str(path)) as container:
        stream = container.streams.audio[0]
        resampler = av.AudioResampler(format="flt", layout="stereo", rate=sample_rate)
        chunks = []
        for frame in container.decode(stream):
            chunks.extend(f.to_ndarray() for f in resampler.resample(frame))
        chunks.extend(f.to_ndarray() for f in resampler.resample(None))  # flush
    if not chunks:
        return np.zeros((0, CHANNELS), np.float32)
    # Packed "flt" frames come as (1, frames * channels), interleaved.
    return np.concatenate(chunks, axis=1).reshape(-1, CHANNELS).astype(np.float32, copy=False)


def trim_with_fade(
    audio: np.ndarray, sample_rate: int, max_seconds: float | None, fade_seconds: float = 1.5
) -> np.ndarray:
    """Cut `audio` to `max_seconds` and fade the end out so it does not stop abruptly."""
    if max_seconds is None or len(audio) <= int(max_seconds * sample_rate):
        return audio
    audio = audio[: int(max_seconds * sample_rate)].copy()
    fade = min(len(audio), int(fade_seconds * sample_rate))
    if fade:
        ramp = np.linspace(1.0, 0.0, fade, dtype=np.float32)
        audio[-fade:] *= ramp[:, None] if audio.ndim == 2 else ramp
    return audio


class FilePlayer:
    def __init__(self, path: Path, max_seconds: float | None = 10.0) -> None:
        self.path = path
        self.max_seconds = max_seconds
        self._audio: np.ndarray | None = None

    def load(self) -> bool:
        """Decode the file once. Returns False if it does not exist."""
        if not self.path.is_file():
            return False
        if self._audio is None:
            self._audio = trim_with_fade(decode(self.path), PLAYBACK_RATE, self.max_seconds)
        return True

    def start(self) -> bool:
        """Start playing without blocking. Returns False if there is nothing to play."""
        if not self.load():
            return False
        import sounddevice as sd

        sd.play(self._audio, PLAYBACK_RATE)
        return True

    @staticmethod
    def wait() -> None:
        import sounddevice as sd

        sd.wait()
