import queue

import numpy as np

from jarvis.trigger.microphone import MicrophoneStream, put_dropping_oldest, to_mono


def test_to_mono_averages_channels():
    stereo = np.array([[1.0, 0.0], [0.5, 0.5]], dtype=np.float32)
    mono = to_mono(stereo)
    assert mono.dtype == np.float32
    np.testing.assert_allclose(mono, [0.5, 0.5])


def test_to_mono_copies_input():
    # PortAudio reuses its buffer after the callback returns.
    data = np.ones((4, 1), dtype=np.float32)
    mono = to_mono(data)
    data[:] = 0
    np.testing.assert_allclose(mono, 1.0)


def test_put_dropping_oldest_keeps_newest():
    blocks = queue.Queue(maxsize=2)
    assert not put_dropping_oldest(blocks, 1)
    assert not put_dropping_oldest(blocks, 2)
    assert put_dropping_oldest(blocks, 3)
    assert [blocks.get_nowait(), blocks.get_nowait()] == [2, 3]


def test_callback_queues_blocks_and_counts_drops():
    mic = MicrophoneStream(max_queued_blocks=1)
    mic._callback(np.full((3, 1), 0.1, dtype=np.float32), 3, None, 0)
    mic._callback(np.full((3, 1), 0.2, dtype=np.float32), 3, None, 1)
    assert mic.dropped_blocks == 1
    assert mic.status_flags == 1
    np.testing.assert_allclose(mic.read(timeout=0), 0.2)
