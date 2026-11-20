"""Localhost protection (TC-57, TC-58, TC-59)."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def raw_client(data_dir: Path) -> TestClient:
    """Client WITHOUT the X-Fitting-Room header."""
    return TestClient(create_app(), base_url="http://localhost")


@pytest.mark.parametrize("host", ["localhost", "127.0.0.1", "localhost:8000", "127.0.0.1:5173"])
def test_local_hosts_allowed(raw_client: TestClient, host: str) -> None:
    assert raw_client.get("/health", headers={"Host": host}).status_code == 200


@pytest.mark.parametrize("host", ["evil.example", "192.168.1.20:8000", "localhost.evil.example"])
def test_other_hosts_rejected(raw_client: TestClient, host: str) -> None:
    """TC-57: blocks DNS rebinding and LAN access."""
    assert raw_client.get("/health", headers={"Host": host}).status_code == 400


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_writes_without_header_rejected(raw_client: TestClient, method: str) -> None:
    """TC-58"""
    response = raw_client.request(method, "/garments")
    assert response.status_code == 403
    assert response.json() == {"detail": "Missing X-Fitting-Room header"}


def test_wrong_header_value_rejected(raw_client: TestClient) -> None:
    assert raw_client.post("/garments", headers={"X-Fitting-Room": "yes"}).status_code == 403


def test_write_with_header_reaches_the_route(raw_client: TestClient) -> None:
    # /garments has no POST route, so passing the guard gives 405 (not 403).
    assert raw_client.post("/garments", headers={"X-Fitting-Room": "1"}).status_code == 405


def test_reads_do_not_need_the_header(raw_client: TestClient) -> None:
    assert raw_client.get("/garments").status_code == 200


def test_no_cors_for_other_origins(raw_client: TestClient) -> None:
    """TC-59: a preflight from another website gets no Access-Control-Allow-* headers."""
    response = raw_client.options(
        "/garments",
        headers={
            "Origin": "https://evil.example",
            "Access-Control-Request-Method": "DELETE",
            "Access-Control-Request-Headers": "x-fitting-room",
        },
    )
    assert not any(h.lower().startswith("access-control-allow") for h in response.headers)
    plain = raw_client.get("/garments", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in plain.headers
