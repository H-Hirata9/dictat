from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout,
    QComboBox, QTextEdit, QLineEdit, QLabel,
)

_FMT_ENGINES = [
    ("verbatim", "そのまま（整形なし）"),
    ("openai", "OpenAI GPT"),
    ("gemini", "Google Gemini"),
]
_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"]
_GEMINI_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
_DEFAULT_TEMPLATE = "以下の音声文字起こしを自然な文章に整形してください:\n\n{text}"


class TemplateTab(QWidget):
    def __init__(self, config, parent=None) -> None:
        super().__init__(parent)
        self._config = config
        layout = QVBoxLayout(self)

        group = QGroupBox("テキスト整形")
        form = QFormLayout(group)

        self._fmt = QComboBox()
        for val, label in _FMT_ENGINES:
            self._fmt.addItem(label, val)
        self._fmt.setCurrentIndex(
            next((i for i, (v, _) in enumerate(_FMT_ENGINES) if v == config.get("output.formatting")), 0)
        )
        form.addRow("整形エンジン", self._fmt)

        self._model = QLineEdit(config.get("formatting.model", "gpt-4o-mini"))
        form.addRow("モデル", self._model)

        self._tmpl = QTextEdit()
        self._tmpl.setPlainText(config.get("formatting.template", _DEFAULT_TEMPLATE))
        self._tmpl.setMinimumHeight(130)
        form.addRow("テンプレート", self._tmpl)

        layout.addWidget(group)
        hint = QLabel("{text} の部分が文字起こし結果に置換されます。")
        layout.addWidget(hint)
        layout.addStretch()

    def save(self) -> None:
        self._config.set("output.formatting", self._fmt.currentData())
        self._config.set("formatting.model", self._model.text().strip())
        self._config.set("formatting.template", self._tmpl.toPlainText())
