"""Request/response models. JSON uses camelCase to match the TypeScript types."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from app.db.models import Garment


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


# ---- Auth -------------------------------------------------------------------

PASSWORD_MIN = 10
PASSWORD_MAX = 128


class Credentials(ApiModel):
    email: EmailStr = Field(max_length=320)
    password: str = Field(min_length=1, max_length=PASSWORD_MAX)

    @field_validator("email")
    @classmethod
    def _normalise_email(cls, value: str) -> str:
        return value.strip().lower()


class SignupRequest(Credentials):
    password: str = Field(min_length=PASSWORD_MIN, max_length=PASSWORD_MAX)


class UserOut(ApiModel):
    id: uuid.UUID
    email: str
    created_at: datetime


# ---- Consent ----------------------------------------------------------------

CONSENT_SCOPE = "capture_and_store_body_model"


class ConsentRequest(ApiModel):
    version: str = Field(max_length=32)
    # Both on-screen checkboxes from docs/consent-v1.md must be ticked.
    confirms_adult_and_self: bool
    agrees_to_capture_and_storage: bool


class ConsentOut(ApiModel):
    id: uuid.UUID
    version: str
    scope: str
    granted_at: datetime
    withdrawn_at: datetime | None


class ConsentStatus(ApiModel):
    required_version: str
    accepted: bool
    consents: list[ConsentOut]


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
