"""ORM models. Every model lives (or is imported) here so Alembic can see it.

Data model reference: docs/02-architecture.md §2.4 (single user, CR-02: no users/sessions/consents)
"""

from datetime import datetime

from sqlalchemy import JSON, Boolean, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDPrimaryKey, utcnow


class AuditLog(UUIDPrimaryKey, Base):
    """What happened to which resource. Single-user prototype: no user column (CR-02)."""

    __tablename__ = "audit_log"

    action: Mapped[str] = mapped_column(String(64))  # e.g. "scan.create", "data.discard"
    target: Mapped[str | None] = mapped_column(String(128), default=None)  # opaque id only
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


GARMENT_CATEGORIES = ("top", "bottom")  # MVP: shirts and pants only


class Garment(Base):
    """Public catalog item. Spec: docs/garment-format.md"""

    __tablename__ = "garments"
    __table_args__ = (CheckConstraint("category IN ('top', 'bottom')", name="category"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # kebab-case slug
    name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(16), index=True)
    model_url: Mapped[str] = mapped_column(String(255))
    thumbnail_url: Mapped[str] = mapped_column(String(255))
    colors: Mapped[list[str]] = mapped_column(JSON, default=list)
    sizes: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_author: Mapped[str] = mapped_column(String(120))
    source_license: Mapped[str] = mapped_column(String(64))
    source_url: Mapped[str | None] = mapped_column(String(255), default=None)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


JOB_STATUSES = ("queued", "processing", "done", "failed")


class Job(UUIDPrimaryKey, Base):
    """Background job (e.g. 3D reconstruction). Processed by app.worker, one at a time."""

    __tablename__ = "jobs"
    __table_args__ = (
        CheckConstraint("status IN ('queued', 'processing', 'done', 'failed')", name="status"),
        CheckConstraint("progress BETWEEN 0 AND 100", name="progress"),
    )

    type: Mapped[str] = mapped_column(String(64))
    ref_id: Mapped[str | None] = mapped_column(String(64), default=None)  # e.g. body_model id
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(16), default="queued", index=True)
    progress: Mapped[int] = mapped_column(default=0)
    step: Mapped[str | None] = mapped_column(String(64), default=None)
    error: Mapped[str | None] = mapped_column(String(500), default=None)  # user-safe message
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    started_at: Mapped[datetime | None] = mapped_column(default=None)
    finished_at: Mapped[datetime | None] = mapped_column(default=None)
