"""Save a scan: create, upload photos (retake = upload again), complete, read current."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.api.deps import DbSession
from app.api.schemas import ScanOut
from app.db.models import SCAN_VIEWS, Scan, ScanImage
from app.services import scans as scan_service
from app.services.audit import audit
from app.services.images import MAX_UPLOAD_BYTES, ImageRejected, clean_image
from app.services.storage import StorageService, get_storage

router = APIRouter(prefix="/scans", tags=["scans"])
Storage = Annotated[StorageService, Depends(get_storage)]


def _out(scan: Scan) -> ScanOut:
    return ScanOut(
        id=scan.id,
        status=scan.status,  # type: ignore[arg-type]
        created_at=scan.created_at,
        completed_at=scan.completed_at,
        images=sorted(scan.images, key=lambda i: SCAN_VIEWS.index(i.view)),  # type: ignore[arg-type]
        missing_views=scan_service.missing_views(scan),
    )


def _capturing_scan(db: DbSession, scan_id: uuid.UUID) -> Scan:
    scan = scan_service.get_scan(db, scan_id)
    if scan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scan not found")
    if scan.status != "capturing":
        raise HTTPException(status.HTTP_409_CONFLICT, "This scan is already saved")
    return scan


@router.post("", response_model=ScanOut, status_code=status.HTTP_201_CREATED)
def create_scan(db: DbSession) -> ScanOut:
    scan = Scan()
    db.add(scan)
    db.flush()
    audit(db, "scan.create", str(scan.id))
    db.commit()
    return _out(scan)


@router.get("/current", response_model=ScanOut)
def get_current_scan(db: DbSession) -> ScanOut:
    scan = scan_service.current_scan(db)
    if scan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No saved scan")
    return _out(scan)


@router.post("/{scan_id}/images", response_model=ScanOut, status_code=status.HTTP_201_CREATED)
async def upload_image(
    scan_id: uuid.UUID,
    db: DbSession,
    storage: Storage,
    view: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
) -> ScanOut:
    scan = _capturing_scan(db, scan_id)
    if view not in SCAN_VIEWS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Unknown view: {view}")
    raw = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "Image is larger than 8 MB")
    try:
        clean = clean_image(raw)
    except ImageRejected as exc:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, str(exc)) from None

    # Retake: replace the earlier photo of this view.
    for old in [i for i in scan.images if i.view == view]:
        storage.delete(old.storage_key)
        scan.images.remove(old)
    db.flush()
    scan.images.append(
        ScanImage(
            view=view,
            storage_key=storage.put(clean.data),
            width=clean.width,
            height=clean.height,
            size_bytes=len(clean.data),
        )
    )
    db.commit()
    db.refresh(scan)
    return _out(scan)


@router.delete("/{scan_id}/images/{image_id}", response_model=ScanOut)
def delete_image(
    scan_id: uuid.UUID, image_id: uuid.UUID, db: DbSession, storage: Storage
) -> ScanOut:
    scan = _capturing_scan(db, scan_id)
    image = next((i for i in scan.images if i.id == image_id), None)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found")
    storage.delete(image.storage_key)
    scan.images.remove(image)
    db.commit()
    db.refresh(scan)
    return _out(scan)


@router.post("/{scan_id}/complete", response_model=ScanOut)
def complete(scan_id: uuid.UUID, db: DbSession, storage: Storage) -> ScanOut:
    scan = _capturing_scan(db, scan_id)
    missing = scan_service.missing_views(scan)
    if missing:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, f"Missing views: {', '.join(missing)}"
        )
    scan_service.complete_scan(db, storage, scan)
    audit(db, "scan.save", str(scan.id))
    db.commit()
    db.refresh(scan)
    return _out(scan)
