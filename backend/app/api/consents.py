"""Grant, view and withdraw consent for capture and storage of body data."""

import uuid

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import AppSettings, CurrentUser, DbSession
from app.api.schemas import CONSENT_SCOPE, ConsentOut, ConsentRequest, ConsentStatus
from app.db.models import Consent
from app.services import consent as consent_service
from app.services.audit import audit

router = APIRouter(prefix="/consents", tags=["consents"])


@router.post("", response_model=ConsentOut, status_code=status.HTTP_201_CREATED)
def grant(body: ConsentRequest, user: CurrentUser, db: DbSession, settings: AppSettings) -> Consent:
    if body.version != settings.consent_version:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Consent text has changed. Please review version {settings.consent_version}.",
        )
    if not (body.confirms_adult_and_self and body.agrees_to_capture_and_storage):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Both boxes must be ticked")

    existing = consent_service.active_consent(db, user, settings.consent_version)
    if existing:
        return existing

    consent = Consent(user_id=user.id, version=body.version, scope=CONSENT_SCOPE)
    db.add(consent)
    db.flush()
    audit(db, user.id, "consent.grant", str(consent.id))
    db.commit()
    return consent


@router.get("/me", response_model=ConsentStatus)
def my_consents(user: CurrentUser, db: DbSession, settings: AppSettings) -> ConsentStatus:
    consents = db.scalars(
        select(Consent).where(Consent.user_id == user.id).order_by(Consent.granted_at.desc())
    ).all()
    return ConsentStatus(
        required_version=settings.consent_version,
        accepted=consent_service.active_consent(db, user, settings.consent_version) is not None,
        consents=[ConsentOut.model_validate(c) for c in consents],
    )


@router.delete("/{consent_id}", status_code=status.HTTP_204_NO_CONTENT)
def withdraw(consent_id: uuid.UUID, user: CurrentUser, db: DbSession) -> None:
    consent = db.get(Consent, consent_id)
    # 404 (not 403) for other users' consents, so ids can't be probed.
    if consent is None or consent.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Consent not found")
    if consent.withdrawn_at is None:
        consent_service.withdraw(db, consent)
        audit(db, user.id, "consent.withdraw", str(consent.id))
        db.commit()
