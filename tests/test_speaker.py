from jarvis.tts.speaker import MODEL_ID, OUTPUT_FORMAT, Speaker, whole_frames


def test_whole_frames_carries_split_samples():
    assert list(whole_frames([b"\x01\x02\x03", b"\x04", b"\x05"])) == [b"\x01\x02", b"\x03\x04"]


def test_whole_frames_skips_empty_pieces():
    assert list(whole_frames([b"", b"\x01", b"\x02"])) == [b"\x01\x02"]


class FakeTextToSpeech:
    def __init__(self):
        self.calls = []

    def stream(self, voice_id, **kwargs):
        self.calls.append((voice_id, kwargs))
        return iter([b"\x00\x01\x02", b"\x03"])


class FakeClient:
    def __init__(self):
        self.text_to_speech = FakeTextToSpeech()


def test_stream_pcm_requests_flash_pcm_with_voice():
    client = FakeClient()
    speaker = Speaker(api_key="unused", voice_id="voice-1", client=client)
    assert b"".join(speaker.stream_pcm("Good evening, sir.")) == b"\x00\x01\x02\x03"
    voice_id, kwargs = client.text_to_speech.calls[0]
    assert voice_id == "voice-1"
    assert kwargs["text"] == "Good evening, sir."
    assert kwargs["model_id"] == MODEL_ID
    assert kwargs["output_format"] == OUTPUT_FORMAT
