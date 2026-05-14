from collections.abc import Callable
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt


def _make_icon(color: str, size: int = 22) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, size - 4, size - 4)
    painter.end()
    return QIcon(pixmap)


class SystemTray(QSystemTrayIcon):
    def __init__(self, on_settings: Callable, on_quit: Callable) -> None:
        super().__init__()
        self._icon_idle = _make_icon("#4CAF50")
        self._icon_recording = _make_icon("#F44336")

        self.setIcon(self._icon_idle)
        self.setToolTip("dictat")

        menu = QMenu()
        menu.addAction("設定", on_settings)
        menu.addSeparator()
        menu.addAction("終了", on_quit)
        self.setContextMenu(menu)
        self.show()

    def set_recording(self, recording: bool) -> None:
        if recording:
            self.setIcon(self._icon_recording)
            self.setToolTip("dictat — 録音中...")
        else:
            self.setIcon(self._icon_idle)
            self.setToolTip("dictat")
