from openai import OpenAI

from .base import AbstractFormatter


class OpenAIFormatter(AbstractFormatter):
    def __init__(self, api_key: str, model: str, template: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._template = template

    def format(self, text: str) -> str:
        prompt = self._template.format(text=text)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
        )
        return (response.choices[0].message.content or "").strip()
