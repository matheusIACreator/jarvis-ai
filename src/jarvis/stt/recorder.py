"""Cut one spoken command out of a stream of microphone blocks.

Waits for speech to start (block RMS clearly above the background noise floor), keeps a
short pre-roll so the first syllable is not lost, and stops after a stretch of silence.
Pure logic over numpy blocks, so it is testable without a microphone.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from jarvis.trigger.microphone import SAMPLE_RATE


@dataclass(frozen=True)
class RecorderSettings:
    sample_rate: int = SAMPLE_RATE
    speech_ratio: float = 3.0  # block RMS must exceed noise floor times this
    min_speech_rms: float = 0.01  # and this absolute level (full scale is 1.0)
    silence_after: float = 0.8  # seconds of silence that end the command
    max_duration: float = 12.0  # hard cap on one command
    wait_timeout: float | None = 5.0  # None: listen until speech or the stream ends
    pre_roll: float = 0.3  # audio kept from just before speech starts
    noise_floor_alpha: float = 0.1
    min_noise_floor: float = 0.002


def _rms(block: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(block, dtype=np.float64)))) if len(block) else 0.0


def record_utterance(
    blocks: Iterable[np.ndarray], settings: RecorderSettings | None = None
) -> np.ndarray | None:
    """Consume blocks until one command is captured. Returns None if no speech came."""
    s = settings or RecorderSettings()
    floor = s.min_noise_floor
    waited = 0.0
    pre_roll: deque[np.ndarray] = deque()
    pre_roll_samples = 0
    captured: list[np.ndarray] = []
    speech_seconds = silence = 0.0

    for block in blocks:
        seconds = len(block) / s.sample_rate
        level = _rms(block)
        is_speech = level >= max(s.min_speech_rms, floor * s.speech_ratio)

        if not captured:
            if not is_speech:
                floor = max(s.min_noise_floor, (1 - s.noise_floor_alpha) * floor + s.noise_floor_alpha * level)
                pre_roll.append(block)
                pre_roll_samples += len(block)
                while pre_roll and pre_roll_samples - len(pre_roll[0]) >= s.pre_roll * s.sample_rate:
                    pre_roll_samples -= len(pre_roll.popleft())
                waited += seconds
                if s.wait_timeout is not None and waited >= s.wait_timeout:
                    return None
                continue
            captured.extend(pre_roll)

        captured.append(block)
        speech_seconds += seconds
        silence = 0.0 if is_speech else silence + seconds
        if silence >= s.silence_after or speech_seconds >= s.max_duration:
            break

    if not captured:
        return None
    return np.concatenate(captured).astype(np.float32, copy=False)
