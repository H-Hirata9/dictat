from abc import ABC, abstractmethod
import numpy as np


class AbstractTranscriber(ABC):
    @abstractmethod
    def transcribe(self, audio: np.ndarray) -> str: ...
