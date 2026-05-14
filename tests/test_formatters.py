import pytest
from unittest.mock import MagicMock, patch
from dictat.formatting.verbatim import VerbatimFormatter


def test_verbatim_returns_text_unchanged():
    fmt = VerbatimFormatter()
    assert fmt.format("hello world") == "hello world"


def test_verbatim_returns_empty_string():
    assert VerbatimFormatter().format("") == ""


def test_verbatim_preserves_whitespace():
    text = "  hello\nworld  "
    assert VerbatimFormatter().format(text) == text


class TestOpenAIFormatter:
    def _make_formatter(self, mock_client):
        from dictat.formatting.openai_fmt import OpenAIFormatter
        with patch("dictat.formatting.openai_fmt.OpenAI", return_value=mock_client):
            return OpenAIFormatter(api_key="sk-test", model="gpt-4o-mini", template="{text}")

    def test_calls_chat_completions(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="formatted text"))]
        )
        fmt = self._make_formatter(mock_client)
        result = fmt.format("raw text")
        assert result == "formatted text"
        mock_client.chat.completions.create.assert_called_once()

    def test_template_substitution(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="ok"))]
        )
        from dictat.formatting.openai_fmt import OpenAIFormatter
        with patch("dictat.formatting.openai_fmt.OpenAI", return_value=mock_client):
            fmt = OpenAIFormatter(api_key="sk", model="m", template="整形: {text}")
        fmt.format("input")
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["content"] == "整形: input"

    def test_strips_whitespace(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="  result  "))]
        )
        fmt = self._make_formatter(mock_client)
        assert fmt.format("x") == "result"


class TestGeminiFormatter:
    def _make_formatter(self, mock_client):
        from dictat.formatting.gemini_fmt import GeminiFormatter
        with patch("dictat.formatting.gemini_fmt.genai") as mock_genai:
            mock_genai.Client.return_value = mock_client
            fmt = GeminiFormatter(api_key="gm-key", model="gemini-2.0-flash", template="{text}")
            fmt._client = mock_client
        return fmt

    def test_calls_generate_content(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MagicMock(text="  result  ")
        fmt = self._make_formatter(mock_client)
        result = fmt.format("input")
        assert result == "result"
        mock_client.models.generate_content.assert_called_once()
