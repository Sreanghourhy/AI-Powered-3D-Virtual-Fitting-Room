"""Request/response models. JSON uses camelCase to match the TypeScript types."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel


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
