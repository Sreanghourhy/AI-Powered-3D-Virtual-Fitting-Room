"""Password hashing and session tokens."""

import hashlib
import secrets
from datetime import UTC, datetime

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_hasher = PasswordHasher()  # Argon2id with library-recommended parameters

# Used when the email is unknown, so login takes the same time either way.
_DUMMY_HASH = _hasher.hash("timing-equaliser-not-a-real-password")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except (VerificationError, InvalidHashError):
        return False


def password_needs_rehash(password_hash: str) -> bool:
    return _hasher.check_needs_rehash(password_hash)


def new_session_token() -> str:
    """Random token sent to the browser in the session cookie (never stored)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Only this hash is stored, so a leaked database can't be used to log in."""
    return hashlib.sha256(token.encode()).hexdigest()


def as_utc(value: datetime) -> datetime:
    """SQLite returns naive datetimes; treat them as UTC."""
    return value if value.tzinfo else value.replace(tzinfo=UTC)
