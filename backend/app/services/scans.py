"""Scan bookkeeping: one current saved scan, encrypted photos."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import BODY_VIEWS, FACE_VIEWS, Scan
from app.services.storage import StorageService

MIN_FACE_VIEWS = 3


def delete_scan(db: Session, storage: StorageService, scan: Scan) -> None:
    for image in scan.images:
        storage.delete(image.storage_key)
    db.delete(scan)


def missing_views(scan: Scan) -> list[str]:
    """Views still needed before a scan can be saved (all 8 body + ≥ 3 face)."""
    have = {image.view for image in scan.images}
    missing = [v for v in BODY_VIEWS if v not in have]
    faces = [v for v in FACE_VIEWS if v in have]
    if len(faces) < MIN_FACE_VIEWS:
        missing += [v for v in FACE_VIEWS if v not in have][: MIN_FACE_VIEWS - len(faces)]
    return missing


def complete_scan(db: Session, storage: StorageService, scan: Scan) -> None:
    """Mark as saved and delete every other scan (single current scan)."""
    scan.status = "saved"
    scan.completed_at = datetime.now(UTC)
    for other in db.scalars(select(Scan).where(Scan.id != scan.id)):
        delete_scan(db, storage, other)


def current_scan(db: Session) -> Scan | None:
    return db.scalars(
        select(Scan).where(Scan.status == "saved").order_by(Scan.completed_at.desc())
    ).first()


def get_scan(db: Session, scan_id: uuid.UUID) -> Scan | None:
    return db.get(Scan, scan_id)
