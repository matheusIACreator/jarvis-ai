"""Continuous capture from the laptop microphone.

`MicrophoneStream` yields mono float32 blocks in [-1, 1]. Blocks are produced on the
PortAudio thread and handed over through a bounded queue; when the consumer falls behind,
the oldest block is dropped so the stream always stays close to real time.
"""

from __future__ import annotations

import queue
from collections.abc import Iterator

import numpy as np

SAMPLE_RATE = 16_000  # Hz; also what faster-whisper expects.
BLOCK_SIZE = 512  # samples per block, 32 ms at 16 kHz.
MAX_QUEUED_BLOCKS = 64  # ~2 s of audio.


def to_mono(block: np.ndarray) -> np.ndarray:
    """Return a 1-D float32 copy of a (frames, channels) block, averaging the channels."""
    if block.ndim == 1:
        return block.astype(np.float32, copy=True)
    return block.mean(axis=1, dtype=np.float32)


def put_dropping_oldest(blocks: queue.Queue, block: np.ndarray) -> bool:
    """Put `block` without blocking. Returns True if an older block had to be dropped."""
    dropped = False
    while True:
        try:
            blocks.put_nowait(block)
            return dropped
        except queue.Full:
            try:
                blocks.get_nowait()
                dropped = True
            except queue.Empty:
                pass


class MicrophoneStream:
    """Context manager and iterator over microphone blocks.

    with MicrophoneStream() as mic:
        for block in mic:
            ...
    """

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        block_size: int = BLOCK_SIZE,
        device: int | str | None = None,
        max_queued_blocks: int = MAX_QUEUED_BLOCKS,
    ) -> None:
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.device = device
        self.dropped_blocks = 0
        self.status_flags = 0
        self._blocks: queue.Queue[np.ndarray] = queue.Queue(maxsize=max_queued_blocks)
        self._stream = None

    def _callback(self, indata, frames, time, status) -> None:
        # Runs on the PortAudio thread: keep it short and never block.
        if status:
            self.status_flags += 1
        if put_dropping_oldest(self._blocks, to_mono(indata)):
            self.dropped_blocks += 1

    def start(self) -> None:
        import sounddevice as sd  # Imported here so the module loads without audio hardware.

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            device=self.device,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def read(self, timeout: float | None = None) -> np.ndarray:
        """Return the next block; raises `queue.Empty` if none arrives within `timeout`."""
        return self._blocks.get(timeout=timeout)

    def __iter__(self) -> Iterator[np.ndarray]:
        while self._stream is not None:
            try:
                yield self.read(timeout=0.5)
            except queue.Empty:
                continue

    def __enter__(self) -> MicrophoneStream:
        self.start()
        return self

    def __exit__(self, *exc_info) -> None:
        self.stop()
