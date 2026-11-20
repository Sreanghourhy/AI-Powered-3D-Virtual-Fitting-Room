"""Discard everything personal: scans, images, models, jobs, outfit and all blobs (CR-02).

Tables holding scan data are listed in DISCARD_MODELS. Every new table that stores
scan-derived data (Phase 3+: scans, scan_images, body_models, outfit) MUST be added here.
The catalog (garments) is not personal data and is kept.
"""

from dataclasses import dataclass

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.models import AuditLog, Job
from app.services.audit import audit
from app.services.storage import StorageService

# Delete order: children before parents.
DISCARD_MODELS: list[type[Base]] = [Job, AuditLog]


@dataclass
class DiscardResult:
    rows: int
    files: int


def discard_all(db: Session, storage: StorageService) -> DiscardResult:
    rows = 0
    for model in DISCARD_MODELS:
        rows += db.execute(delete(model)).rowcount or 0
    db.commit()
    # Files after the DB commit: if this fails, re-running Discard removes the rest.
    files = storage.delete_all()
    audit(db, "data.discard")  # no ids, no personal data
    db.commit()
    return DiscardResult(rows=rows, files=files)
