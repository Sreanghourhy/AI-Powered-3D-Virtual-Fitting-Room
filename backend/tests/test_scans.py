"""Milestone 1: saving scans (upload, retake, limits, metadata removal, complete, discard)."""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.db.models import BODY_VIEWS, FACE_VIEWS
from app.services.storage import get_storage


def jpeg_bytes(size: tuple[int, int] = (64, 48), with_gps: bool = False) -> bytes:
    img = Image.new("RGB", size, (200, 120, 80))
    out = io.BytesIO()
    if with_gps:
        exif = Image.Exif()
        exif[0x010F] = "SecretCameraMaker"  # Make
        exif[0x8825] = {1: "N", 2: (13.0, 30.0, 0.0)}  # GPS IFD
        img.save(out, format="JPEG", exif=exif)
    else:
        img.save(out, format="JPEG")
    return out.getvalue()


def png_bytes() -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (20, 10), (0, 0, 255)).save(out, format="PNG")
    return out.getvalue()


def new_scan(client: TestClient) -> str:
    response = client.post("/scans")
    assert response.status_code == 201
    assert response.json()["status"] == "capturing"
    return response.json()["id"]


def upload(client: TestClient, scan_id: str, view: str, data: bytes | None = None):  # noqa: ANN201
    return client.post(
        f"/scans/{scan_id}/images",
        data={"view": view},
        files={"file": ("photo.jpg", data or jpeg_bytes(), "image/jpeg")},
    )


def fill(client: TestClient, scan_id: str, faces: int = 3) -> None:
    for view in BODY_VIEWS + FACE_VIEWS[:faces]:
        assert upload(client, scan_id, view).status_code == 201


def blob_files(data_dir: Path) -> list[Path]:
    root = data_dir / "blobs"
    return [p for p in root.rglob("*") if p.is_file()] if root.exists() else []


def test_upload_stores_encrypted_photo_without_metadata(client: TestClient, data_dir: Path) -> None:
    scan_id = new_scan(client)
    response = upload(client, scan_id, "front", jpeg_bytes(with_gps=True))
    assert response.status_code == 201
    image = response.json()["images"][0]
    assert (image["view"], image["width"], image["height"]) == ("front", 64, 48)

    files = blob_files(data_dir)
    assert len(files) == 1
    raw_on_disk = files[0].read_bytes()
    assert b"\xff\xd8\xff" not in raw_on_disk[:16]  # not a plain JPEG
    assert b"SecretCameraMaker" not in raw_on_disk

    stored = get_storage().get(files[0].name)
    with Image.open(io.BytesIO(stored)) as img:
        assert img.format == "JPEG"
        assert dict(img.getexif()) == {}  # all metadata removed
    assert b"SecretCameraMaker" not in stored


def test_png_is_accepted_and_converted(client: TestClient) -> None:
    scan_id = new_scan(client)
    assert upload(client, scan_id, "back", png_bytes()).status_code == 201


def test_retake_replaces_the_view(client: TestClient, data_dir: Path) -> None:
    scan_id = new_scan(client)
    upload(client, scan_id, "front", jpeg_bytes((10, 10)))
    body = upload(client, scan_id, "front", jpeg_bytes((30, 20))).json()
    assert len(body["images"]) == 1
    assert body["images"][0]["width"] == 30
    assert len(blob_files(data_dir)) == 1  # old photo deleted


def test_delete_single_image(client: TestClient, data_dir: Path) -> None:
    scan_id = new_scan(client)
    image_id = upload(client, scan_id, "left").json()["images"][0]["id"]
    assert client.delete(f"/scans/{scan_id}/images/{image_id}").json()["images"] == []
    assert blob_files(data_dir) == []


@pytest.mark.parametrize(
    ("view", "data", "status"),
    [
        ("sideways", None, 422),  # unknown view
        ("front", b"MZ\x90\x00 not an image", 415),  # wrong signature
        ("front", b"\xff\xd8\xff" + b"broken", 415),  # JPEG header, unreadable body
        ("front", b"\xff\xd8\xff" + b"0" * (8 * 1024 * 1024), 413),  # too large
    ],
)
def test_bad_uploads_rejected(
    client: TestClient, view: str, data: bytes | None, status: int
) -> None:
    scan_id = new_scan(client)
    assert upload(client, scan_id, view, data).status_code == status


def test_unknown_scan_is_404(client: TestClient) -> None:
    assert upload(client, "00000000-0000-0000-0000-000000000000", "front").status_code == 404


def test_complete_requires_all_body_views_and_three_faces(client: TestClient) -> None:
    scan_id = new_scan(client)
    fill(client, scan_id, faces=2)
    response = client.post(f"/scans/{scan_id}/complete")
    assert response.status_code == 422
    assert "face_" in response.json()["detail"]


def test_complete_saves_and_becomes_current(client: TestClient) -> None:
    assert client.get("/scans/current").status_code == 404
    scan_id = new_scan(client)
    fill(client, scan_id)
    body = client.post(f"/scans/{scan_id}/complete").json()
    assert body["status"] == "saved"
    assert body["missingViews"] == []
    current = client.get("/scans/current").json()
    assert current["id"] == scan_id
    assert [i["view"] for i in current["images"]][:2] == ["front", "front_right"]
    assert upload(client, scan_id, "front").status_code == 409  # saved scans are read-only


def test_new_saved_scan_replaces_the_old_one(client: TestClient, data_dir: Path) -> None:
    first = new_scan(client)
    fill(client, first)
    client.post(f"/scans/{first}/complete")
    second = new_scan(client)
    fill(client, second, faces=5)
    client.post(f"/scans/{second}/complete")
    assert client.get("/scans/current").json()["id"] == second
    assert len(blob_files(data_dir)) == len(BODY_VIEWS) + 5  # first scan's photos deleted


def test_discard_removes_scans_and_photos(client: TestClient, data_dir: Path) -> None:
    scan_id = new_scan(client)
    fill(client, scan_id)
    client.post(f"/scans/{scan_id}/complete")
    assert client.delete("/data").status_code == 204
    assert client.get("/scans/current").status_code == 404
    assert blob_files(data_dir) == []
