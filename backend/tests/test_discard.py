"""Discard scan & model (TC-44, Q10)."""

from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.db.models import AuditLog, Garment, Job
from app.db.seed import seed_garments
from app.db.session import session_factory
from app.services.discard import DISCARD_MODELS
from app.services.jobs import enqueue
from app.services.storage import get_storage


def _blob_files(data_dir: Path) -> list[Path]:
    blobs = data_dir / "blobs"
    return [p for p in blobs.rglob("*") if p.is_file()] if blobs.exists() else []


def test_discard_removes_all_rows_and_files(client: TestClient, data_dir: Path) -> None:
    storage = get_storage()
    for _ in range(3):
        storage.put(b"\xff\xd8\xff fake scan image")
    with session_factory()() as db:
        seed_garments(db)
        enqueue(db, job_type="sleep")
        enqueue(db, job_type="sleep")
        db.commit()
    assert len(_blob_files(data_dir)) == 3

    assert client.delete("/data").status_code == 204

    assert _blob_files(data_dir) == []
    with session_factory()() as db:
        assert db.scalar(select(func.count()).select_from(Job)) == 0
        # Catalog is not personal data and stays.
        assert db.scalar(select(func.count()).select_from(Garment)) == 4
        # Only the discard event itself remains in the audit log, without ids.
        logs = db.scalars(select(AuditLog)).all()
        assert [(log.action, log.target) for log in logs] == [("data.discard", None)]


def test_discard_is_idempotent(client: TestClient) -> None:
    assert client.delete("/data").status_code == 204
    assert client.delete("/data").status_code == 204


def test_discard_requires_write_header(data_dir: Path) -> None:
    from app.main import create_app

    raw = TestClient(create_app(), base_url="http://localhost")
    assert raw.delete("/data").status_code == 403


def test_every_table_except_catalog_is_discarded() -> None:
    """Guard: a new table holding scan data must be added to DISCARD_MODELS."""
    from app.db.base import Base

    kept = {"garments"}
    discarded = {model.__tablename__ for model in DISCARD_MODELS}
    assert set(Base.metadata.tables) - kept == discarded
