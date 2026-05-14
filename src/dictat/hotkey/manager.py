from collections.abc import Callable
from pynput import keyboard

_MODIFIERS = {"ctrl", "shift", "alt", "cmd", "win"}


def _build_combo(keys: list[str]) -> str:
    parts = [f"<{k}>" if k.lower() in _MODIFIERS else k for k in keys]
    return "+".join(parts)


class HotkeyManager:
    def __init__(self, keys: list[str], on_activate: Callable[[], None]) -> None:
        self._keys = keys
        self._on_activate = on_activate
        self._listener: keyboard.GlobalHotKeys | None = None

    def start(self) -> None:
        combo = _build_combo(self._keys)
        self._listener = keyboard.GlobalHotKeys({combo: self._on_activate})
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener = None

    def update(self, keys: list[str]) -> None:
        self.stop()
        self._keys = keys
        self.start()
