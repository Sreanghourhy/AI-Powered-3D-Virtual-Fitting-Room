"""Discard all captured images and generated data (FR-11)."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession
from app.services.discard import discard_all
from app.services.storage import StorageService, get_storage

router = APIRouter(prefix="/data", tags=["data"])


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def discard(db: DbSession, storage: Annotated[StorageService, Depends(get_storage)]) -> None:
    discard_all(db, storage)
