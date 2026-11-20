"""Application settings, loaded from environment variables / backend/.env.

All variables use the ``FR_`` prefix, e.g. ``FR_ENCRYPTION_KEY``.
"""

import base64
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FR_",
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="development", pattern="^(development|test|production)$")

    # Private customer data lives here (git-ignored). Never inside static/.
    data_dir: Path = REPO_ROOT / "data"
    database_url: str | None = None

    # 32-byte key, base64-encoded. Generate with: python -m app.core.keys
    encryption_key: str = Field(min_length=1)

    session_cookie_name: str = "fr_session"
    session_ttl_days: int = 14
    cookie_secure: bool = True

    consent_version: str = "consent-v2"  # docs/consent-v2.md (MacBook camera)

    @field_validator("encryption_key")
    @classmethod
    def _check_key(cls, value: str) -> str:
        try:
            raw = base64.urlsafe_b64decode(value.encode())
        except ValueError as exc:
            raise ValueError("FR_ENCRYPTION_KEY must be base64") from exc
        if len(raw) != 32:
            raise ValueError("FR_ENCRYPTION_KEY must decode to exactly 32 bytes")
        return value

    @property
    def encryption_key_bytes(self) -> bytes:
        return base64.urlsafe_b64decode(self.encryption_key.encode())

    @property
    def db_url(self) -> str:
        return self.database_url or f"sqlite:///{self.data_dir / 'app.db'}"

    @property
    def blobs_dir(self) -> Path:
        return self.data_dir / "blobs"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]  # values come from the environment
