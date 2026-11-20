"""Consent rules (docs/consent-v2.md, docs/03-privacy-security.md §3.1)."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas import CONSENT_SCOPE
from app.db.models import Consent, User


def active_consent(db: Session, user: User, version: str) -> Consent | None:
    """The user's current, not-withdrawn consent for the required version."""
    return db.scalars(
        select(Consent).where(
            Consent.user_id == user.id,
            Consent.version == version,
            Consent.scope == CONSENT_SCOPE,
            Consent.withdrawn_at.is_(None),
        )
    ).first()


def withdraw(db: Session, consent: Consent) -> None:
    consent.withdrawn_at = datetime.now(UTC)
    # Withdrawing consent must delete the user's scan data (consent-v2, "Your choices").
    # Captures and body models don't exist until Phase 3/4. Their deletion is wired here
    # when those tables are added (tracked in docs/tasks/phase-3-capture.md, P3-02).
