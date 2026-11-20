"""Helpers shared by API tests."""

from fastapi.testclient import TestClient

PASSWORD = "correct-horse-1"


def signup(client: TestClient, email: str = "alice@example.com") -> dict:
    response = client.post("/auth/signup", json={"email": email, "password": PASSWORD})
    assert response.status_code == 201, response.text
    return response.json()


CONSENT_VERSION = "consent-v2"


def accept_consent(client: TestClient, version: str = CONSENT_VERSION) -> dict:
    response = client.post(
        "/consents",
        json={"version": version, "confirmsAdultAndSelf": True, "agreesToCaptureAndStorage": True},
    )
    assert response.status_code == 201, response.text
    return response.json()
