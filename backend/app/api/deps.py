"""Shared FastAPI dependencies."""

from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import as_utc, hash_token
from app.db.models import User, UserSession
from app.db.session import get_db

DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def get_current_session(request: Request, db: DbSession, settings: AppSettings) -> UserSession:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not signed in")

    session = db.scalars(
        select(UserSession).where(UserSession.token_hash == hash_token(token))
    ).one_or_none()
    if session is None or as_utc(session.expires_at) <= datetime.now(UTC):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not signed in")
    if session.user.deleted_at is not None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not signed in")
    return session


CurrentSession = Annotated[UserSession, Depends(get_current_session)]


def get_current_user(session: CurrentSession) -> User:
    return session.user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_consent(user: CurrentUser, db: DbSession, settings: AppSettings) -> User:
    """Guard for capture endpoints: user must have accepted the current consent version."""
    from app.services.consent import active_consent

    if active_consent(db, user, settings.consent_version) is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Consent required before capture")
    return user


ConsentedUser = Annotated[User, Depends(require_consent)]
