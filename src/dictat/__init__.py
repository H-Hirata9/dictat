import sys
from .app import DictatApp


def main() -> None:
    app = DictatApp()
    sys.exit(app.run())
