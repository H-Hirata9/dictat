import io
import wave
import numpy as np
import pytest
from unittest.mock import MagicMock, patch


def _silence(seconds: float = 1.0) -> np.ndarray:
    return np.zeros(int(16000 * seconds), dtype=np.float32)


class TestWhisperAPITranscriber:
    def _make(self, mock_client):
        from dictat.transcription.whisper_api import WhisperAPITranscriber
        with patch("dictat.transcription.whisper_api.OpenAI", return_value=mock_client):
            return WhisperAPITranscriber(api_key="sk-test", language="ja")

    def test_returns_transcription_text(self):
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create.return_value = MagicMock(text="  hello  ")
        t = self._make(mock_client)
        result = t.transcribe(_silence())
        assert result == "hello"

    def test_sends_wav_file(self):
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create.return_value = MagicMock(text="ok")
        t = self._make(mock_client)
        t.transcribe(_silence())
        call_kwargs = mock_client.audio.transcriptions.create.call_args.kwargs
        assert call_kwargs["model"] == "whisper-1"
        assert call_kwargs["language"] == "ja"
        # Verify the file is a WAV
        file_obj = call_kwargs["file"]
        file_obj.seek(0)
        with wave.open(file_obj) as wf:
            assert wf.getnchannels() == 1


class TestElevenLabsTranscriber:
    def _make(self, mock_client):
        from dictat.transcription.elevenlabs import ElevenLabsTranscriber
        with patch("dictat.transcription.elevenlabs.ElevenLabs", return_value=mock_client):
            return ElevenLabsTranscriber(api_key="el-key", language="ja")

    def test_returns_transcription_text(self):
        mock_client = MagicMock()
        mock_client.speech_to_text.convert.return_value = MagicMock(text="  result  ")
        t = self._make(mock_client)
        assert t.transcribe(_silence()) == "result"

    def test_uses_scribe_v1_model(self):
        mock_client = MagicMock()
        mock_client.speech_to_text.convert.return_value = MagicMock(text="ok")
        t = self._make(mock_client)
        t.transcribe(_silence())
        call_kwargs = mock_client.speech_to_text.convert.call_args.kwargs
        assert call_kwargs["model_id"] == "scribe_v1"
        assert call_kwargs["language_code"] == "ja"
