import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.core.keys import new_key


def test_settings_load_from_env() -> None:
    settings = Settings()  # type: ignore[call-arg]
    assert settings.environment == "test"
    assert len(settings.encryption_key_bytes) == 32
    assert settings.db_url.startswith("sqlite:///")


def test_rejects_short_encryption_key() -> None:
    with pytest.raises(ValidationError):
        Settings(encryption_key="dG9vLXNob3J0")  # type: ignore[call-arg]


def test_generated_key_is_valid() -> None:
    assert len(Settings(encryption_key=new_key()).encryption_key_bytes) == 32  # type: ignore[call-arg]
