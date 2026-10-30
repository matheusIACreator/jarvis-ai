"""Double hand-clap detection on a stream of mono audio blocks.

A clap is a short, sharp burst: its peak is high in absolute terms and far above the
background noise floor (RMS of quiet blocks), and it is quiet again within
`max_clap_duration`. Peak is used rather than block RMS because a clap lasts only a few
milliseconds and averaging over a whole block would hide it. Longer loud sounds (speech,
music, a door slam with echo) are rejected. Two claps separated by `min_gap..max_gap`
seconds fire the trigger, followed by a cooldown.

Time is counted in samples, so behaviour is deterministic and testable offline.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from jarvis.trigger.microphone import SAMPLE_RATE


@dataclass(frozen=True)
class ClapSettings:
    sample_rate: int = SAMPLE_RATE
    min_peak: float = 0.25  # absolute peak a clap must reach (full scale is 1.0)
    threshold_ratio: float = 10.0  # peak must exceed noise floor times this
    max_clap_duration: float = 0.12  # seconds a clap may stay loud
    min_gap: float = 0.12  # seconds between the two clap onsets
    max_gap: float = 0.8
    cooldown: float = 1.5  # seconds ignored after a trigger
    noise_floor_alpha: float = 0.05  # EMA weight for quiet blocks
    min_noise_floor: float = 0.002


class ClapDetector:
    def __init__(self, settings: ClapSettings | None = None) -> None:
        self.settings = settings or ClapSettings()
        self.noise_floor = self.settings.min_noise_floor
        self._samples = 0
        self._loud_start: float | None = None
        self._sustained = False
        self._last_clap: float | None = None
        self._cooldown_until = 0.0

    @property
    def now(self) -> float:
        return self._samples / self.settings.sample_rate

    def process(self, block: np.ndarray) -> bool:
        """Feed one mono block. Returns True when a double clap completes."""
        s = self.settings
        start = self.now
        self._samples += len(block)
        if len(block) == 0:
            return False

        rms = float(np.sqrt(np.mean(np.square(block, dtype=np.float64))))
        peak = float(np.max(np.abs(block)))
        loud = peak >= max(s.min_peak, self.noise_floor * s.threshold_ratio)

        if loud:
            if self._loud_start is None:
                self._loud_start = start
            elif self.now - self._loud_start > s.max_clap_duration:
                # Too long to be a clap; it also breaks any pending pair.
                self._sustained = True
                self._last_clap = None
            return False

        self._update_noise_floor(rms)
        onset, sustained = self._loud_start, self._sustained
        self._loud_start, self._sustained = None, False
        if onset is not None and not sustained:
            return self._register_clap(onset)
        return False

    def _update_noise_floor(self, rms: float) -> None:
        a = self.settings.noise_floor_alpha
        self.noise_floor = max(self.settings.min_noise_floor, (1 - a) * self.noise_floor + a * rms)

    def _register_clap(self, onset: float) -> bool:
        s = self.settings
        if onset < self._cooldown_until:
            return False
        if self._last_clap is not None:
            gap = onset - self._last_clap
            if s.min_gap <= gap <= s.max_gap:
                self._last_clap = None
                self._cooldown_until = onset + s.cooldown
                return True
        self._last_clap = onset
        return False
