from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.models import AuditLog, User, UserSession
from app.db.session import session_factory
from tests.helpers import PASSWORD, signup


def test_signup_creates_user_and_secure_session_cookie(client: TestClient) -> None:
    response = client.post(
        "/auth/signup", json={"email": " Alice@Example.COM ", "password": PASSWORD}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert set(body) == {"id", "email", "createdAt"}  # never returns the password hash

    cookie = response.headers["set-cookie"].lower()
    assert "fr_session=" in cookie
    assert "httponly" in cookie
    assert "secure" in cookie
    assert "samesite=lax" in cookie


def test_password_is_hashed_with_argon2(client: TestClient) -> None:
    signup(client)
    with session_factory()() as db:
        user = db.scalars(select(User)).one()
        assert user.password_hash.startswith("$argon2id$")
        assert PASSWORD not in user.password_hash


def test_session_token_is_stored_hashed(client: TestClient) -> None:
    signup(client)
    token = client.cookies["fr_session"]
    with session_factory()() as db:
        stored = db.scalars(select(UserSession)).one()
        assert stored.token_hash != token
        assert len(stored.token_hash) == 64


def test_duplicate_email_rejected(client: TestClient) -> None:
    signup(client)
    response = client.post(
        "/auth/signup", json={"email": "ALICE@example.com", "password": PASSWORD}
    )
    assert response.status_code == 409
    with session_factory()() as db:
        assert len(db.scalars(select(User)).all()) == 1


def test_short_password_rejected(client: TestClient) -> None:
    response = client.post("/auth/signup", json={"email": "a@example.com", "password": "short"})
    assert response.status_code == 422


def test_invalid_email_rejected(client: TestClient) -> None:
    response = client.post("/auth/signup", json={"email": "not-an-email", "password": PASSWORD})
    assert response.status_code == 422


def test_me_requires_login(client: TestClient) -> None:
    assert client.get("/auth/me").status_code == 401


def test_me_returns_current_user(client: TestClient) -> None:
    user = signup(client)
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["id"] == user["id"]


def test_login_success(client: TestClient) -> None:
    signup(client)
    client.cookies.clear()
    response = client.post("/auth/login", json={"email": "alice@example.com", "password": PASSWORD})
    assert response.status_code == 200
    assert client.get("/auth/me").status_code == 200


def test_wrong_password_and_unknown_email_get_same_error(client: TestClient) -> None:
    signup(client)
    client.cookies.clear()
    wrong = client.post(
        "/auth/login", json={"email": "alice@example.com", "password": "nope-nope-1"}
    )
    unknown = client.post("/auth/login", json={"email": "bob@example.com", "password": PASSWORD})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json() == {"detail": "Email or password is wrong"}
    assert "set-cookie" not in wrong.headers


def test_logout_ends_session(client: TestClient) -> None:
    signup(client)
    token = client.cookies["fr_session"]
    assert client.post("/auth/logout").status_code == 204
    # The old token no longer works even if replayed.
    client.cookies.set("fr_session", token)
    assert client.get("/auth/me").status_code == 401


def test_expired_session_rejected(client: TestClient) -> None:
    signup(client)
    with session_factory()() as db:
        session = db.scalars(select(UserSession)).one()
        session.expires_at = datetime.now(UTC) - timedelta(seconds=1)
        db.commit()
    assert client.get("/auth/me").status_code == 401


def test_deleted_user_cannot_login_or_use_session(client: TestClient) -> None:
    signup(client)
    with session_factory()() as db:
        db.scalars(select(User)).one().deleted_at = datetime.now(UTC)
        db.commit()
    assert client.get("/auth/me").status_code == 401
    client.cookies.clear()
    response = client.post("/auth/login", json={"email": "alice@example.com", "password": PASSWORD})
    assert response.status_code == 401


def test_auth_events_are_audited(client: TestClient) -> None:
    signup(client)
    client.post("/auth/logout")
    with session_factory()() as db:
        actions = [log.action for log in db.scalars(select(AuditLog).order_by(AuditLog.created_at))]
    assert actions == ["auth.signup", "auth.logout"]
