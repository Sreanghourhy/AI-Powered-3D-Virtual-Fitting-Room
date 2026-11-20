"""Request/response models. JSON uses camelCase to match the TypeScript types."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from app.db.models import Garment


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


# ---- Garments (matches src/lib/types/garment.ts) ---------------------------

GarmentCategory = Literal["top", "bottom"]


class GarmentSourceOut(ApiModel):
    author: str
    license: str
    url: str | None = None


class GarmentOut(ApiModel):
    id: str
    name: str
    category: GarmentCategory
    model_url: str
    thumbnail_url: str
    colors: list[str]
    sizes: list[str]
    source: GarmentSourceOut
    active: bool

    @classmethod
    def from_model(cls, garment: "Garment") -> "GarmentOut":
        return cls(
            id=garment.id,
            name=garment.name,
            category=garment.category,  # type: ignore[arg-type]
            model_url=garment.model_url,
            thumbnail_url=garment.thumbnail_url,
            colors=garment.colors,
            sizes=garment.sizes,
            source=GarmentSourceOut(
                author=garment.source_author,
                license=garment.source_license,
                url=garment.source_url,
            ),
            active=garment.active,
        )


# ---- Jobs -------------------------------------------------------------------


class JobOut(ApiModel):
    id: uuid.UUID
    type: str
    status: Literal["queued", "processing", "done", "failed"]
    progress: int
    step: str | None
    error: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None


# ---- Scans (Milestone 1) ---------------------------------------------------


class ScanImageOut(ApiModel):
    id: uuid.UUID
    view: str
    width: int
    height: int
    size_bytes: int


class ScanOut(ApiModel):
    id: uuid.UUID
    status: Literal["capturing", "saved"]
    created_at: datetime
    completed_at: datetime | None
    images: list[ScanImageOut]
    missing_views: list[str]
