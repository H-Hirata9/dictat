import json
import os
from pathlib import Path
from typing import Any

_DEFAULT: dict[str, Any] = {
    "transcription": {
        "engine": "whisper_local",
        "whisper_model": "base",
        "language": "ja",
    },
    "output": {
        "formatting": "verbatim",
    },
    "formatting": {
        "engine": "openai",
        "model": "gpt-4o-mini",
        "template": "以下の音声文字起こしを自然な文章に整形してください:\n\n{text}",
    },
    "hotkey": {
        "keys": ["ctrl", "shift", "r"],
    },
}


class Config:
    def __init__(self) -> None:
        app_data = Path(os.environ.get("APPDATA", Path.home())) / "dictat"
        app_data.mkdir(parents=True, exist_ok=True)
        self._path = app_data / "config.json"
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            try:
                with open(self._path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split(".")
        val = self._data
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                val = None
                break
        if val is not None:
            return val
        val = _DEFAULT
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val

    def set(self, key: str, value: Any) -> None:
        parts = key.split(".")
        d = self._data
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value
        self._save()
