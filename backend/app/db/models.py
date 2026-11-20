"""ORM models. Every model lives (or is imported) here so Alembic can see it.

Data model reference: docs/02-architecture.md §2.4 (single user, CR-02: no users/sessions/consents)
"""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


# Milestone 1: 8 body views (turning 45° each) + 5 face close-ups.
BODY_VIEWS = (
    "front", "front_right", "right", "back_right", "back", "back_left", "left", "front_left",
)  # fmt: skip
FACE_VIEWS = ("face_front", "face_left_45", "face_right_45", "face_left_90", "face_right_90")
SCAN_VIEWS = BODY_VIEWS + FACE_VIEWS


class Scan(UUIDPrimaryKey, Base):
    """One capture session. Only one 'saved' scan is kept (single-user prototype)."""

    __tablename__ = "scans"
    __table_args__ = (CheckConstraint("status IN ('capturing', 'saved')", name="status"),)

    status: Mapped[str] = mapped_column(String(16), default="capturing", index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(default=None)

    images: Mapped[list["ScanImage"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan", passive_deletes=True
    )


class ScanImage(UUIDPrimaryKey, Base):
    """One photo of a scan, stored encrypted (storage_key → data/blobs)."""

    __tablename__ = "scan_images"
    __table_args__ = (UniqueConstraint("scan_id", "view", name="scan_view"),)

    scan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scans.id", ondelete="CASCADE"), index=True
    )
    view: Mapped[str] = mapped_column(String(32))
    storage_key: Mapped[str] = mapped_column(String(32))
    width: Mapped[int]
    height: Mapped[int]
    size_bytes: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    scan: Mapped[Scan] = relationship(back_populates="images")
