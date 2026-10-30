"""Speak text out loud with ElevenLabs, playing audio while it is still being generated.

Audio is requested as raw 16-bit PCM so chunks can go straight to the speaker through
`sounddevice`, with no MP3 decoding step.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator

MODEL_ID = "eleven_flash_v2_5"  # lowest latency (~75 ms)
OUTPUT_FORMAT = "pcm_24000"
SAMPLE_RATE = 24_000
BYTES_PER_FRAME = 2  # mono int16


def whole_frames(chunks: Iterable[bytes], frame_size: int = BYTES_PER_FRAME) -> Iterator[bytes]:
    """Re-chunk a byte stream so every piece holds whole frames.

    Network chunks can split a sample in half; the leftover byte is carried to the next chunk.
    """
    pending = b""
    for chunk in chunks:
        data = pending + chunk
        cut = len(data) - len(data) % frame_size
        pending = data[cut:]
        if cut:
            yield data[:cut]


class Speaker:
    def __init__(
        self,
        api_key: str,
        voice_id: str,
        model_id: str = MODEL_ID,
        client=None,
    ) -> None:
        if client is None:
            from elevenlabs import ElevenLabs

            client = ElevenLabs(api_key=api_key)
        self.client = client
        self.voice_id = voice_id
        self.model_id = model_id

    def stream_pcm(self, text: str) -> Iterator[bytes]:
        """Yield raw PCM (24 kHz, mono, int16) for `text`, in whole frames."""
        from elevenlabs import VoiceSettings

        chunks = self.client.text_to_speech.stream(
            self.voice_id,
            text=text,
            model_id=self.model_id,
            output_format=OUTPUT_FORMAT,
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        )
        return whole_frames(chunks)

    def speak(self, text: str) -> None:
        """Say `text` on the default output device; blocks until playback ends."""
        import sounddevice as sd

        with sd.RawOutputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as out:
            for chunk in self.stream_pcm(text):
                out.write(chunk)
