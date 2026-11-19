import stat
from pathlib import Path

import pytest

from app.core.keys import new_key
from app.services.storage import StorageError, StorageService, get_storage

JPEG_MAGIC = b"\xff\xd8\xff\xe0"
GLB_MAGIC = b"glTF"


@pytest.fixture
def storage(tmp_path: Path) -> StorageService:
    return StorageService(tmp_path / "blobs", b"k" * 32)


def test_round_trip(storage: StorageService) -> None:
    data = JPEG_MAGIC + b"fake photo bytes" * 100
    key = storage.put(data)
    assert storage.get(key) == data


def test_file_on_disk_is_not_plaintext(storage: StorageService, tmp_path: Path) -> None:
    data = GLB_MAGIC + b"secret body model" * 50
    key = storage.put(data)
    raw = (tmp_path / "blobs" / key[:2] / key).read_bytes()
    assert raw.startswith(b"FR1")
    assert GLB_MAGIC not in raw
    assert b"secret body model" not in raw


def test_keys_are_random_and_opaque(storage: StorageService) -> None:
    keys = {storage.put(b"same") for _ in range(20)}
    assert len(keys) == 20
    assert all(len(k) == 32 and k.isalnum() for k in keys)


def test_files_are_owner_only(storage: StorageService, tmp_path: Path) -> None:
    key = storage.put(b"x")
    mode = (tmp_path / "blobs" / key[:2] / key).stat().st_mode
    assert stat.S_IMODE(mode) == 0o600


def test_delete_removes_file(storage: StorageService, tmp_path: Path) -> None:
    key = storage.put(b"x")
    assert storage.delete(key) is True
    assert not storage.exists(key)
    assert not (tmp_path / "blobs" / key[:2] / key).exists()
    assert storage.delete(key) is False
    with pytest.raises(StorageError):
        storage.get(key)


def test_tampered_blob_rejected(storage: StorageService, tmp_path: Path) -> None:
    key = storage.put(b"original")
    path = tmp_path / "blobs" / key[:2] / key
    raw = bytearray(path.read_bytes())
    raw[-1] ^= 0x01
    path.write_bytes(bytes(raw))
    with pytest.raises(StorageError):
        storage.get(key)


def test_blob_moved_to_another_key_rejected(storage: StorageService, tmp_path: Path) -> None:
    key_a = storage.put(b"user A data")
    key_b = storage.put(b"user B data")
    path_a = tmp_path / "blobs" / key_a[:2] / key_a
    path_b = tmp_path / "blobs" / key_b[:2] / key_b
    path_b.write_bytes(path_a.read_bytes())
    with pytest.raises(StorageError):
        storage.get(key_b)


def test_wrong_encryption_key_cannot_decrypt(tmp_path: Path) -> None:
    key = StorageService(tmp_path, b"a" * 32).put(b"secret")
    with pytest.raises(StorageError):
        StorageService(tmp_path, b"b" * 32).get(key)


@pytest.mark.parametrize("bad", ["../../etc/passwd", "ABC", "", "0" * 31, "g" * 32])
def test_invalid_keys_rejected(storage: StorageService, bad: str) -> None:
    with pytest.raises(StorageError):
        storage.get(bad)


def test_get_storage_uses_data_dir(data_dir: Path) -> None:
    storage = get_storage()
    key = storage.put(b"x")
    assert (data_dir / "blobs" / key[:2] / key).is_file()


def test_rejects_wrong_key_length(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        StorageService(tmp_path, b"short")
    assert new_key()  # generator still usable
