import io
import numpy as np
from elevenlabs import ElevenLabs

from .base import AbstractTranscriber
from ..audio.recorder import to_wav_bytes


class ElevenLabsTranscriber(AbstractTranscriber):
    def __init__(self, api_key: str, language: str | None = "ja") -> None:
        self._client = ElevenLabs(api_key=api_key)
        self._language = language

    def transcribe(self, audio: np.ndarray) -> str:
        buf = io.BytesIO(to_wav_bytes(audio))
        result = self._client.speech_to_text.convert(
            file=buf,
            model_id="scribe_v1",
            language_code=self._language,
        )
        return result.text.strip()
