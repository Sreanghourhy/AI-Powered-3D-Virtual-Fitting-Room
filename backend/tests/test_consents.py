from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from app.api.deps import ConsentedUser
from app.main import create_app
from tests.helpers import CONSENT_VERSION, accept_consent, signup


def test_consent_requires_login(client: TestClient) -> None:
    assert client.get("/consents/me").status_code == 401


def test_new_user_has_no_consent(client: TestClient) -> None:
    signup(client)
    body = client.get("/consents/me").json()
    assert body == {"requiredVersion": CONSENT_VERSION, "accepted": False, "consents": []}


def test_accept_consent_stores_version_and_time(client: TestClient) -> None:
    signup(client)
    consent = accept_consent(client)
    assert consent["version"] == CONSENT_VERSION
    assert consent["scope"] == "capture_and_store_body_model"
    assert consent["grantedAt"]
    assert consent["withdrawnAt"] is None
    assert client.get("/consents/me").json()["accepted"] is True


def test_accepting_twice_returns_same_consent(client: TestClient) -> None:
    signup(client)
    assert accept_consent(client)["id"] == accept_consent(client)["id"]
    assert len(client.get("/consents/me").json()["consents"]) == 1


def test_both_checkboxes_required(client: TestClient) -> None:
    signup(client)
    response = client.post(
        "/consents",
        json={
            "version": CONSENT_VERSION,
            "confirmsAdultAndSelf": True,
            "agreesToCaptureAndStorage": False,
        },
    )
    assert response.status_code == 422


def test_outdated_version_rejected(client: TestClient) -> None:
    signup(client)
    response = client.post(
        "/consents",
        json={
            "version": "consent-v0",
            "confirmsAdultAndSelf": True,
            "agreesToCaptureAndStorage": True,
        },
    )
    assert response.status_code == 409


def test_withdraw_consent(client: TestClient) -> None:
    signup(client)
    consent = accept_consent(client)
    assert client.delete(f"/consents/{consent['id']}").status_code == 204
    status = client.get("/consents/me").json()
    assert status["accepted"] is False
    assert status["consents"][0]["withdrawnAt"] is not None


def test_cannot_withdraw_another_users_consent(client: TestClient) -> None:
    signup(client, "alice@example.com")
    alice_consent = accept_consent(client)
    client.cookies.clear()
    signup(client, "bob@example.com")
    assert client.delete(f"/consents/{alice_consent['id']}").status_code == 404


# ---- require_consent guard (used by capture endpoints in Phase 3) -------------


def _app_with_protected_route() -> FastAPI:
    app = create_app()
    router = APIRouter()

    @router.get("/_test/protected")
    def protected(user: ConsentedUser) -> dict:
        return {"ok": True}

    app.include_router(router)
    return app


def test_guard_blocks_user_without_consent(data_dir: Path) -> None:
    with TestClient(_app_with_protected_route(), base_url="https://testserver") as client:
        signup(client)
        assert client.get("/_test/protected").status_code == 403


def test_guard_allows_user_with_consent(data_dir: Path) -> None:
    with TestClient(_app_with_protected_route(), base_url="https://testserver") as client:
        signup(client)
        accept_consent(client)
        assert client.get("/_test/protected").status_code == 200


def test_guard_blocks_after_withdrawal(data_dir: Path) -> None:
    with TestClient(_app_with_protected_route(), base_url="https://testserver") as client:
        signup(client)
        consent = accept_consent(client)
        client.delete(f"/consents/{consent['id']}")
        assert client.get("/_test/protected").status_code == 403


def test_older_consent_version_requires_reconsent(client: TestClient) -> None:
    """Users who accepted v1 (phone wording) must accept v2 before capture."""
    import uuid

    from app.db.models import Consent
    from app.db.session import session_factory

    user = signup(client)
    with session_factory()() as db:
        db.add(
            Consent(
                user_id=uuid.UUID(user["id"]),
                version="consent-v1",
                scope="capture_and_store_body_model",
            )
        )
        db.commit()
    status = client.get("/consents/me").json()
    assert status["accepted"] is False
    assert status["consents"][0]["version"] == "consent-v1"
    accept_consent(client)
    assert client.get("/consents/me").json()["accepted"] is True
