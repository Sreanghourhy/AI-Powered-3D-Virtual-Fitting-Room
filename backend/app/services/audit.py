"""Audit log helper. Store opaque ids only, never personal data."""

import uuid

from sqlalchemy.orm import Session

from app.db.models import AuditLog


def audit(db: Session, user_id: uuid.UUID | None, action: str, target: str | None = None) -> None:
    db.add(AuditLog(user_id=user_id, action=action, target=target))
