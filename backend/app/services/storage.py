"""Encrypted file storage for private customer data (scans, 3D models).

Every file is encrypted with AES-256-GCM before it touches disk. Files are named
by a random opaque ``storage_key`` (never a user name, email or original filename).
The key is also bound to the ciphertext as associated data, so a blob copied or
renamed to another key fails to decrypt.

On-disk format:  b"FR1" | 12-byte nonce | ciphertext + 16-byte tag
"""

import os
import re
import secrets
import tempfile
from functools import lru_cache
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import get_settings

MAGIC = b"FR1"
NONCE_SIZE = 12
_KEY_PATTERN = re.compile(r"^[0-9a-f]{32}$")


class StorageError(Exception):
    """Raised for missing, invalid or tampered blobs."""


class StorageService:
    def __init__(self, root: Path, key: bytes) -> None:
        if len(key) != 32:
            raise ValueError("Encryption key must be 32 bytes")
        self._root = root
        self._aead = AESGCM(key)

    # -- public API ------------------------------------------------------------

    def put(self, data: bytes) -> str:
        """Encrypt and store ``data``. Returns a new opaque storage key."""
        storage_key = secrets.token_hex(16)
        nonce = secrets.token_bytes(NONCE_SIZE)
        blob = MAGIC + nonce + self._aead.encrypt(nonce, data, storage_key.encode())
        self._write_atomic(self._path(storage_key), blob)
        return storage_key

    def get(self, storage_key: str) -> bytes:
        """Read and decrypt a blob. Raises StorageError if missing or tampered."""
        path = self._path(storage_key)
        try:
            blob = path.read_bytes()
        except FileNotFoundError:
            raise StorageError("Blob not found") from None
        if not blob.startswith(MAGIC) or len(blob) < len(MAGIC) + NONCE_SIZE + 16:
            raise StorageError("Blob is corrupt")
        nonce = blob[len(MAGIC) : len(MAGIC) + NONCE_SIZE]
        try:
            return self._aead.decrypt(nonce, blob[len(MAGIC) + NONCE_SIZE :], storage_key.encode())
        except InvalidTag:
            raise StorageError("Blob failed integrity check") from None

    def delete(self, storage_key: str) -> bool:
        """Delete a blob. Returns False if it did not exist."""
        path = self._path(storage_key)
        try:
            path.unlink()
        except FileNotFoundError:
            return False
        return True

    def exists(self, storage_key: str) -> bool:
        return self._path(storage_key).is_file()

    # -- internals -------------------------------------------------------------

    def _path(self, storage_key: str) -> Path:
        # Strict format check prevents path traversal ("../") via crafted keys.
        if not _KEY_PATTERN.match(storage_key):
            raise StorageError("Invalid storage key")
        return self._root / storage_key[:2] / storage_key

    @staticmethod
    def _write_atomic(path: Path, blob: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(blob)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp, 0o600)
            os.replace(tmp, path)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise


@lru_cache
def _cached_storage(root: str, key: bytes) -> StorageService:
    return StorageService(Path(root), key)


def get_storage() -> StorageService:
    """FastAPI dependency / shared accessor using app settings."""
    settings = get_settings()
    return _cached_storage(str(settings.blobs_dir), settings.encryption_key_bytes)
