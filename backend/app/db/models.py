"""ORM models. Every model lives (or is imported) here so Alembic can see it.

Data model reference: docs/02-architecture.md §2.4
"""

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKey, utcnow


class User(UUIDPrimaryKey, Base):
    __tablename__ = "users"

    # Stored lower-case; uniqueness enforced by the database.
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    consents: Mapped[list["Consent"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


class UserSession(UUIDPrimaryKey, Base):
    """Server-side login session. The cookie holds a random token; we store its SHA-256."""

    __tablename__ = "sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    expires_at: Mapped[datetime]

    user: Mapped[User] = relationship(back_populates="sessions")


class Consent(UUIDPrimaryKey, Base):
    """One row per consent the user granted. Withdrawal is recorded, not deleted."""

    __tablename__ = "consents"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    version: Mapped[str] = mapped_column(String(32))  # e.g. "consent-v1"
    scope: Mapped[str] = mapped_column(String(64))  # e.g. "capture_and_store_body_model"
    granted_at: Mapped[datetime] = mapped_column(default=utcnow)
    withdrawn_at: Mapped[datetime | None] = mapped_column(default=None)

    user: Mapped[User] = relationship(back_populates="consents")


class AuditLog(UUIDPrimaryKey, Base):
    """Who did what to which resource. user_id is nulled (anonymised) on account deletion."""

    __tablename__ = "audit_log"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str] = mapped_column(String(64))  # e.g. "auth.login", "model.delete"
    target: Mapped[str | None] = mapped_column(String(128), default=None)  # opaque id only
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
