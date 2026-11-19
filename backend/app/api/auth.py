"""Sign up, log in, log out, current user."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import AppSettings, CurrentSession, CurrentUser, DbSession
from app.api.schemas import Credentials, SignupRequest, UserOut
from app.core.config import Settings
from app.core.security import (
    hash_password,
    hash_token,
    new_session_token,
    password_needs_rehash,
    verify_password,
)
from app.db.models import User, UserSession
from app.services.audit import audit

router = APIRouter(prefix="/auth", tags=["auth"])

INVALID_LOGIN = "Email or password is wrong"


def _start_session(db: DbSession, user: User, response: Response, settings: Settings) -> None:
    token = new_session_token()
    expires = datetime.now(UTC) + timedelta(days=settings.session_ttl_days)
    db.add(UserSession(user_id=user.id, token_hash=hash_token(token), expires_at=expires))
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_ttl_days * 24 * 3600,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
    )


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, response: Response, db: DbSession, settings: AppSettings) -> User:
    user = User(email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "An account with this email already exists"
        ) from None
    _start_session(db, user, response, settings)
    audit(db, user.id, "auth.signup")
    db.commit()
    return user


@router.post("/login", response_model=UserOut)
def login(body: Credentials, response: Response, db: DbSession, settings: AppSettings) -> User:
    user = db.scalars(
        select(User).where(User.email == body.email, User.deleted_at.is_(None))
    ).one_or_none()
    # verify_password always runs (dummy hash for unknown users) to avoid timing leaks.
    if not verify_password(user.password_hash if user else None, body.password) or user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, INVALID_LOGIN)

    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(body.password)
    _start_session(db, user, response, settings)
    audit(db, user.id, "auth.login")
    db.commit()
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    session: CurrentSession, response: Response, db: DbSession, settings: AppSettings
) -> None:
    audit(db, session.user_id, "auth.logout")
    db.delete(session)
    db.commit()
    response.delete_cookie(
        settings.session_cookie_name,
        path="/",
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
    )


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> User:
    return user
