from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QComboBox,
)

_ENGINES = [
    ("whisper_local", "Whisper（ローカル）"),
    ("whisper_api", "Whisper API（OpenAI）"),
    ("elevenlabs", "ElevenLabs Scribe"),
]
_WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
_LANGUAGES = [("ja", "日本語"), ("en", "English"), ("", "自動検出")]


class ApiKeysTab(QWidget):
    def __init__(self, config, keystore, parent=None) -> None:
        super().__init__(parent)
        self._config = config
        self._keystore = keystore
        layout = QVBoxLayout(self)

        eng_group = QGroupBox("文字起こしエンジン")
        eng_form = QFormLayout(eng_group)

        self._engine = QComboBox()
        for val, label in _ENGINES:
            self._engine.addItem(label, val)
        self._engine.setCurrentIndex(
            next((i for i, (v, _) in enumerate(_ENGINES) if v == config.get("transcription.engine")), 0)
        )
        eng_form.addRow("エンジン", self._engine)

        self._model = QComboBox()
        for m in _WHISPER_MODELS:
            self._model.addItem(m)
        cur_model = config.get("transcription.whisper_model", "base")
        idx = self._model.findText(cur_model)
        self._model.setCurrentIndex(idx if idx >= 0 else 1)
        eng_form.addRow("Whisperモデル", self._model)

        self._lang = QComboBox()
        for val, label in _LANGUAGES:
            self._lang.addItem(label, val)
        cur_lang = config.get("transcription.language", "ja")
        self._lang.setCurrentIndex(
            next((i for i, (v, _) in enumerate(_LANGUAGES) if v == cur_lang), 0)
        )
        eng_form.addRow("言語", self._lang)
        layout.addWidget(eng_group)

        key_group = QGroupBox("APIキー")
        key_form = QFormLayout(key_group)

        self._openai = self._make_key_field(keystore.get("openai"))
        key_form.addRow("OpenAI", self._openai)

        self._elevenlabs = self._make_key_field(keystore.get("elevenlabs"))
        key_form.addRow("ElevenLabs", self._elevenlabs)

        self._gemini = self._make_key_field(keystore.get("gemini"))
        key_form.addRow("Gemini", self._gemini)

        layout.addWidget(key_group)
        layout.addStretch()

    def _make_key_field(self, value: str | None) -> QLineEdit:
        field = QLineEdit(value or "")
        field.setEchoMode(QLineEdit.EchoMode.Password)
        field.setPlaceholderText("sk-...")
        return field

    def save(self) -> None:
        self._config.set("transcription.engine", self._engine.currentData())
        self._config.set("transcription.whisper_model", self._model.currentText())
        self._config.set("transcription.language", self._lang.currentData())

        for attr, provider in [
            (self._openai, "openai"),
            (self._elevenlabs, "elevenlabs"),
            (self._gemini, "gemini"),
        ]:
            val = attr.text().strip()
            if val:
                self._keystore.set(provider, val)
