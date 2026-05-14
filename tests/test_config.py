import json
import pytest
from pathlib import Path
from dictat.storage.config import Config


@pytest.fixture
def config(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    return Config()


def test_default_engine(config):
    assert config.get("transcription.engine") == "whisper_local"


def test_default_hotkey(config):
    assert config.get("hotkey.keys") == ["ctrl", "shift", "r"]


def test_default_formatting(config):
    assert config.get("output.formatting") == "verbatim"


def test_get_missing_key_returns_none(config):
    assert config.get("nonexistent.key") is None


def test_get_missing_key_returns_given_default(config):
    assert config.get("nonexistent.key", "fallback") == "fallback"


def test_set_and_get(config):
    config.set("transcription.engine", "whisper_api")
    assert config.get("transcription.engine") == "whisper_api"


def test_set_persists_to_disk(config, tmp_path):
    config.set("hotkey.keys", ["ctrl", "r"])
    saved = json.loads((tmp_path / "dictat" / "config.json").read_text(encoding="utf-8"))
    assert saved["hotkey"]["keys"] == ["ctrl", "r"]


def test_set_nested_key(config):
    config.set("formatting.model", "gpt-4o")
    assert config.get("formatting.model") == "gpt-4o"


def test_loaded_value_overrides_default(config, tmp_path):
    (tmp_path / "dictat").mkdir(exist_ok=True)
    (tmp_path / "dictat" / "config.json").write_text(
        json.dumps({"transcription": {"engine": "elevenlabs"}}), encoding="utf-8"
    )
    monkeypatched_config = Config.__new__(Config)
    monkeypatched_config._path = tmp_path / "dictat" / "config.json"
    monkeypatched_config._data = json.loads(
        (tmp_path / "dictat" / "config.json").read_text(encoding="utf-8")
    )
    assert monkeypatched_config.get("transcription.engine") == "elevenlabs"
