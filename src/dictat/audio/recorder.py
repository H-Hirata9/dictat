import io
import wave
import numpy as np
import sounddevice as sd

_SAMPLERATE = 16000
_CHANNELS = 1
_DTYPE = "float32"


def to_wav_bytes(audio: np.ndarray, samplerate: int = _SAMPLERATE) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        pcm = (audio * 32767).astype(np.int16)
        wf.writeframes(pcm.tobytes())
    return buf.getvalue()


class AudioRecorder:
    def __init__(self) -> None:
        self._frames: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None

    def _callback(self, indata: np.ndarray, frames: int, time: object, status: object) -> None:
        self._frames.append(indata.copy())

    def start(self) -> None:
        self._frames = []
        self._stream = sd.InputStream(
            samplerate=_SAMPLERATE,
            channels=_CHANNELS,
            dtype=_DTYPE,
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if not self._frames:
            return np.array([], dtype=np.float32)
        return np.concatenate(self._frames, axis=0).flatten()
