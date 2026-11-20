"""Audit log helper. Store opaque ids only, never personal data."""

from sqlalchemy.orm import Session

from app.db.models import AuditLog


def audit(db: Session, action: str, target: str | None = None) -> None:
    db.add(AuditLog(action=action, target=target))
