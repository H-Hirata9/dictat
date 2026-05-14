import sys
import threading
import numpy as np
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from PySide6.QtCore import QObject, Signal

from .audio.recorder import AudioRecorder
from .hotkey.manager import HotkeyManager
from .output.injector import TextInjector
from .storage.config import Config
from .storage.keys import KeyStore
from .ui.tray import SystemTray


class _Signals(QObject):
    set_recording = Signal(bool)
    inject_text = Signal(str)
    show_error = Signal(str)


class DictatApp:
    def __init__(self) -> None:
        self._qapp = QApplication.instance() or QApplication(sys.argv)
        self._qapp.setQuitOnLastWindowClosed(False)

        self._config = Config()
        self._keystore = KeyStore()
        self._recorder = AudioRecorder()
        self._injector = TextInjector()
        self._recording = False
        self._lock = threading.Lock()

        self._sig = _Signals()

        self._tray = SystemTray(
            on_settings=self._open_settings,
            on_quit=self._quit,
        )

        self._sig.set_recording.connect(self._tray.set_recording)
        self._sig.inject_text.connect(self._injector.inject)
        self._sig.show_error.connect(
            lambda msg: self._tray.showMessage(
                "dictat エラー", msg, QSystemTrayIcon.MessageIcon.Critical
            )
        )

        keys = self._config.get("hotkey.keys", ["ctrl", "shift", "r"])
        self._hotkey = HotkeyManager(keys=keys, on_activate=self._toggle)
        self._hotkey.start()

    def _toggle(self) -> None:
        with self._lock:
            if not self._recording:
                self._recording = True
                self._sig.set_recording.emit(True)
                self._recorder.start()
            else:
                self._recording = False
                audio = self._recorder.stop()
                self._sig.set_recording.emit(False)
                if audio.size > 0:
                    threading.Thread(
                        target=self._process, args=(audio,), daemon=True
                    ).start()

    def _process(self, audio: np.ndarray) -> None:
        try:
            transcriber = self._build_transcriber()
            text = transcriber.transcribe(audio)
            formatter = self._build_formatter()
            text = formatter.format(text)
            self._sig.inject_text.emit(text)
        except Exception as exc:
            self._sig.show_error.emit(str(exc))

    def _build_transcriber(self):
        engine = self._config.get("transcription.engine", "whisper_local")
        lang = self._config.get("transcription.language", "ja") or None
        if engine == "whisper_api":
            from .transcription.whisper_api import WhisperAPITranscriber
            return WhisperAPITranscriber(
                api_key=self._keystore.get("openai") or "",
                language=lang,
            )
        if engine == "elevenlabs":
            from .transcription.elevenlabs import ElevenLabsTranscriber
            return ElevenLabsTranscriber(
                api_key=self._keystore.get("elevenlabs") or "",
                language=lang,
            )
        from .transcription.whisper_local import WhisperLocalTranscriber
        return WhisperLocalTranscriber(
            model_name=self._config.get("transcription.whisper_model", "base"),
            language=lang,
        )

    def _build_formatter(self):
        fmt = self._config.get("output.formatting", "verbatim")
        model = self._config.get("formatting.model", "gpt-4o-mini")
        template = self._config.get("formatting.template", "{text}")
        if fmt == "openai":
            from .formatting.openai_fmt import OpenAIFormatter
            return OpenAIFormatter(
                api_key=self._keystore.get("openai") or "",
                model=model,
                template=template,
            )
        if fmt == "gemini":
            from .formatting.gemini_fmt import GeminiFormatter
            return GeminiFormatter(
                api_key=self._keystore.get("gemini") or "",
                model=model,
                template=template,
            )
        from .formatting.verbatim import VerbatimFormatter
        return VerbatimFormatter()

    def _open_settings(self) -> None:
        from .ui.settings.dialog import SettingsDialog
        dlg = SettingsDialog(self._config, self._keystore, self._hotkey)
        dlg.exec()

    def _quit(self) -> None:
        self._hotkey.stop()
        self._qapp.quit()

    def run(self) -> int:
        return self._qapp.exec()
