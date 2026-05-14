from google import genai

from .base import AbstractFormatter


class GeminiFormatter(AbstractFormatter):
    def __init__(self, api_key: str, model: str, template: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._template = template

    def format(self, text: str) -> str:
        prompt = self._template.format(text=text)
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        return response.text.strip()
