import numpy as np
import whisper

from .base import AbstractTranscriber


class WhisperLocalTranscriber(AbstractTranscriber):
    def __init__(self, model_name: str = "base", language: str | None = "ja") -> None:
        self._model_name = model_name
        self._language = language
        self._model: whisper.Whisper | None = None

    def load(self) -> None:
        if self._model is None:
            self._model = whisper.load_model(self._model_name)

    def transcribe(self, audio: np.ndarray) -> str:
        self.load()
        assert self._model is not None
        result = self._model.transcribe(audio, language=self._language)
        return str(result["text"]).strip()
