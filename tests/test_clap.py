import numpy as np

from jarvis.trigger.clap import ClapDetector
from jarvis.trigger.microphone import BLOCK_SIZE, SAMPLE_RATE


def background(seconds, level=0.005, seed=0):
    rng = np.random.default_rng(seed)
    return (rng.standard_normal(int(seconds * SAMPLE_RATE)) * level).astype(np.float32)


def add_clap(signal, at, amplitude=0.8, seed=1):
    """Exponentially decaying noise burst, roughly what a hand clap looks like."""
    rng = np.random.default_rng(seed)
    n = int(0.03 * SAMPLE_RATE)
    t = np.arange(n) / SAMPLE_RATE
    burst = rng.standard_normal(n) * np.exp(-t / 0.005)
    burst = burst / np.max(np.abs(burst)) * amplitude
    i = int(at * SAMPLE_RATE)
    signal[i : i + n] += burst.astype(np.float32)
    return signal


def run(signal):
    detector = ClapDetector()
    triggers = []
    for i in range(0, len(signal), BLOCK_SIZE):
        if detector.process(signal[i : i + BLOCK_SIZE]):
            triggers.append(detector.now)
    return triggers


def test_double_clap_triggers_once():
    signal = add_clap(add_clap(background(2.0), 0.5), 0.85)
    triggers = run(signal)
    assert len(triggers) == 1
    assert 0.85 < triggers[0] < 1.0


def test_quiet_room_never_triggers():
    assert run(background(3.0)) == []


def test_single_clap_does_not_trigger():
    assert run(add_clap(background(2.0), 0.5)) == []


def test_claps_too_far_apart_do_not_trigger():
    assert run(add_clap(add_clap(background(3.0), 0.5), 2.0)) == []


def test_sustained_loud_sound_is_not_a_clap():
    signal = background(2.0)
    rng = np.random.default_rng(2)
    signal[8000:16000] += (rng.standard_normal(8000) * 0.3).astype(np.float32)
    # A loud 0.5 s sound followed by a single clap must not pair up.
    signal = add_clap(signal, 1.3)
    assert run(signal) == []


def test_cooldown_suppresses_extra_claps():
    signal = background(3.0)
    for at in (0.5, 0.8, 1.1, 1.4):
        signal = add_clap(signal, at)
    assert len(run(signal)) == 1


def test_works_over_noisy_background():
    signal = add_clap(add_clap(background(3.0, level=0.03), 1.5), 1.9)
    assert len(run(signal)) == 1


def test_noisy_background_alone_does_not_trigger():
    assert run(background(3.0, level=0.05)) == []
