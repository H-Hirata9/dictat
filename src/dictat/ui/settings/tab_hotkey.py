from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QCheckBox, QLineEdit, QLabel,
)

_MODIFIERS = ["ctrl", "shift", "alt"]


class HotkeyTab(QWidget):
    def __init__(self, config, hotkey_manager, parent=None) -> None:
        super().__init__(parent)
        self._config = config
        self._hotkey_manager = hotkey_manager
        layout = QVBoxLayout(self)

        group = QGroupBox("録音トグルホットキー（最大3キーの組み合わせ）")
        form = QFormLayout(group)

        current = config.get("hotkey.keys", ["ctrl", "shift", "r"])
        self._checks: dict[str, QCheckBox] = {}
        for mod in _MODIFIERS:
            cb = QCheckBox(mod.capitalize())
            cb.setChecked(mod in current)
            self._checks[mod] = cb
            form.addRow("", cb)

        regular = [k for k in current if k not in _MODIFIERS]
        self._key_edit = QLineEdit(regular[0] if regular else "r")
        self._key_edit.setMaxLength(1)
        self._key_edit.setPlaceholderText("a–z, 0–9 など1文字")
        form.addRow("キー", self._key_edit)

        layout.addWidget(group)
        note = QLabel("変更は保存後すぐに反映されます。")
        note.setWordWrap(True)
        layout.addWidget(note)
        layout.addStretch()

    def save(self) -> None:
        keys = [mod for mod, cb in self._checks.items() if cb.isChecked()]
        key_char = self._key_edit.text().strip().lower()
        if key_char:
            keys.append(key_char)
        if keys:
            self._config.set("hotkey.keys", keys)
            self._hotkey_manager.update(keys)
