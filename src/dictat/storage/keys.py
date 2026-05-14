import keyring
import keyring.errors

_SERVICE = "dictat"
_KEY_MAP = {
    "openai": "openai_api_key",
    "elevenlabs": "elevenlabs_api_key",
    "gemini": "gemini_api_key",
}


class KeyStore:
    def get(self, provider: str) -> str | None:
        name = _KEY_MAP.get(provider)
        return keyring.get_password(_SERVICE, name) if name else None

    def set(self, provider: str, value: str) -> None:
        name = _KEY_MAP.get(provider)
        if name:
            keyring.set_password(_SERVICE, name, value)

    def delete(self, provider: str) -> None:
        name = _KEY_MAP.get(provider)
        if name:
            try:
                keyring.delete_password(_SERVICE, name)
            except keyring.errors.PasswordDeleteError:
                pass
