from .base import AbstractFormatter


class VerbatimFormatter(AbstractFormatter):
    def format(self, text: str) -> str:
        return text
