import io
import wave
import numpy as np
import pytest
from dictat.audio.recorder import AudioRecorder, to_wav_bytes


def test_to_wav_bytes_produces_valid_wav():
    audio = np.zeros(16000, dtype=np.float32)
    data = to_wav_bytes(audio)
    with wave.open(io.BytesIO(data)) as wf:
        assert wf.getnchannels() == 1
        assert wf.getframerate() == 16000
        assert wf.getsampwidth() == 2
        assert wf.getnframes() == 16000


def test_to_wav_bytes_encodes_values():
    audio = np.ones(100, dtype=np.float32)
    data = to_wav_bytes(audio)
    with wave.open(io.BytesIO(data)) as wf:
        raw = wf.readframes(100)
    samples = np.frombuffer(raw, dtype=np.int16)
    assert all(s == 32767 for s in samples)


def test_recorder_stop_without_start_returns_empty():
    rec = AudioRecorder()
    result = rec.stop()
    assert result.size == 0
    assert result.dtype == np.float32


def test_recorder_stop_with_no_frames_returns_empty():
    rec = AudioRecorder()
    rec._frames = []
    result = rec.stop()
    assert result.size == 0
