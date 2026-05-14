import pytest
from unittest.mock import patch, MagicMock
from dictat.storage.keys import KeyStore


@pytest.fixture
def store():
    return KeyStore()


def test_get_returns_none_when_empty(store):
    with patch("keyring.get_password", return_value=None):
        assert store.get("openai") is None


def test_get_returns_stored_value(store):
    with patch("keyring.get_password", return_value="sk-test"):
        assert store.get("openai") == "sk-test"


def test_set_calls_keyring(store):
    with patch("keyring.set_password") as mock_set:
        store.set("openai", "sk-abc")
        mock_set.assert_called_once_with("dictat", "openai_api_key", "sk-abc")


def test_set_elevenlabs(store):
    with patch("keyring.set_password") as mock_set:
        store.set("elevenlabs", "el-key")
        mock_set.assert_called_once_with("dictat", "elevenlabs_api_key", "el-key")


def test_set_gemini(store):
    with patch("keyring.set_password") as mock_set:
        store.set("gemini", "gm-key")
        mock_set.assert_called_once_with("dictat", "gemini_api_key", "gm-key")


def test_get_unknown_provider_returns_none(store):
    assert store.get("unknown_provider") is None


def test_delete_calls_keyring(store):
    with patch("keyring.delete_password") as mock_del:
        store.delete("openai")
        mock_del.assert_called_once_with("dictat", "openai_api_key")


def test_delete_swallows_not_found_error(store):
    import keyring.errors
    with patch("keyring.delete_password", side_effect=keyring.errors.PasswordDeleteError):
        store.delete("openai")  # should not raise
