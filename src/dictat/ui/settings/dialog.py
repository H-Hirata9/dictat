from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QDialogButtonBox

from .tab_api import ApiKeysTab
from .tab_hotkey import HotkeyTab
from .tab_template import TemplateTab


class SettingsDialog(QDialog):
    def __init__(self, config, keystore, hotkey_manager, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("dictat — 設定")
        self.setMinimumWidth(520)

        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        self._api_tab = ApiKeysTab(config, keystore)
        self._hotkey_tab = HotkeyTab(config, hotkey_manager)
        self._template_tab = TemplateTab(config)

        tabs.addTab(self._api_tab, "APIキー / エンジン")
        tabs.addTab(self._hotkey_tab, "ホットキー")
        tabs.addTab(self._template_tab, "テンプレート")
        layout.addWidget(tabs)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _save_and_accept(self) -> None:
        self._api_tab.save()
        self._hotkey_tab.save()
        self._template_tab.save()
        self.accept()
