"""Migration tests, incl. the CR-02 upgrade that removes accounts."""

import uuid
from pathlib import Path

from sqlalchemy import inspect, text

from alembic import command
from app.db.migrate import alembic_config
from app.db.session import get_engine

PRE_CR02 = "a6c9f7f0b941"  # last revision that still had users/sessions/consents


def test_head_has_no_account_tables(data_dir: Path) -> None:
    inspector = inspect(get_engine())
    tables = set(inspector.get_table_names())
    assert not tables & {"users", "sessions", "consents"}
    assert "user_id" not in {c["name"] for c in inspector.get_columns("jobs")}
    assert "user_id" not in {c["name"] for c in inspector.get_columns("audit_log")}


def test_upgrade_keeps_jobs_and_audit_rows(data_dir: Path) -> None:
    """Upgrading an existing DB must not cascade-delete jobs when `users` is dropped."""
    cfg = alembic_config()
    command.downgrade(cfg, PRE_CR02)
    user_id = uuid.uuid4().hex
    with get_engine().begin() as conn:
        conn.execute(
            text(
                "INSERT INTO users (id, email, password_hash, created_at) "
                "VALUES (:id, 'a@example.com', 'x', CURRENT_TIMESTAMP)"
            ),
            {"id": user_id},
        )
        conn.execute(
            text(
                "INSERT INTO jobs (id, user_id, type, payload, status, progress, created_at) "
                "VALUES (:id, :uid, 'sleep', '{}', 'done', 100, CURRENT_TIMESTAMP)"
            ),
            {"id": uuid.uuid4().hex, "uid": user_id},
        )
        conn.execute(
            text(
                "INSERT INTO audit_log (id, user_id, action, created_at) "
                "VALUES (:id, :uid, 'auth.signup', CURRENT_TIMESTAMP)"
            ),
            {"id": uuid.uuid4().hex, "uid": user_id},
        )

    command.upgrade(cfg, "head")

    with get_engine().connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM jobs")).scalar() == 1
        assert conn.execute(text("SELECT count(*) FROM audit_log")).scalar() == 1
    assert "users" not in inspect(get_engine()).get_table_names()


def test_downgrade_to_base_on_empty_db(data_dir: Path) -> None:
    command.downgrade(alembic_config(), "base")
    assert set(inspect(get_engine()).get_table_names()) <= {"alembic_version"}
