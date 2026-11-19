from pathlib import Path

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError

from alembic import command
from app.db.migrate import alembic_config
from app.db.models import AuditLog, Consent, User
from app.db.session import get_engine, session_factory


def test_insert_and_read_user(data_dir: Path) -> None:
    with session_factory()() as db:
        db.add(User(email="a@example.com", password_hash="x"))
        db.commit()
        user = db.scalars(select(User).where(User.email == "a@example.com")).one()
        assert user.id is not None
        assert user.created_at is not None
        assert user.deleted_at is None


def test_email_is_unique(data_dir: Path) -> None:
    with session_factory()() as db:
        db.add_all([User(email="a@example.com", password_hash="x")])
        db.commit()
        db.add(User(email="a@example.com", password_hash="y"))
        with pytest.raises(IntegrityError):
            db.commit()


def test_deleting_user_cascades_consents_and_anonymises_audit(data_dir: Path) -> None:
    with session_factory()() as db:
        user = User(email="a@example.com", password_hash="x")
        db.add(user)
        db.flush()
        db.add(Consent(user_id=user.id, version="consent-v1", scope="capture"))
        db.add(AuditLog(user_id=user.id, action="auth.signup"))
        db.commit()

        db.delete(user)
        db.commit()

        assert db.scalars(select(Consent)).all() == []
        log = db.scalars(select(AuditLog)).one()
        assert log.user_id is None
        assert log.action == "auth.signup"


def test_migration_downgrade_to_base(data_dir: Path) -> None:
    command.downgrade(alembic_config(), "base")
    tables = set(inspect(get_engine()).get_table_names())
    assert not tables & {"users", "consents", "audit_log"}
