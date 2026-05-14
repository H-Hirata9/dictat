import time
from pynput.keyboard import Controller, Key


class TextInjector:
    def __init__(self) -> None:
        self._ctrl = Controller()

    def inject(self, text: str) -> None:
        # Small delay to ensure focus has returned after hotkey release
        time.sleep(0.05)
        self._ctrl.type(text)
