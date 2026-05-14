import io
import numpy as np
from openai import OpenAI

from .base import AbstractTranscriber
from ..audio.recorder import to_wav_bytes


class WhisperAPITranscriber(AbstractTranscriber):
    def __init__(self, api_key: str, language: str | None = "ja") -> None:
        self._client = OpenAI(api_key=api_key)
        self._language = language

    def transcribe(self, audio: np.ndarray) -> str:
        buf = io.BytesIO(to_wav_bytes(audio))
        buf.name = "audio.wav"
        response = self._client.audio.transcriptions.create(
            model="whisper-1",
            file=buf,
            language=self._language,
        )
        return response.text.strip()
