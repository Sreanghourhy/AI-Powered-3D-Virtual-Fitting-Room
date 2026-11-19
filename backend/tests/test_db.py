from pathlib import Path

from sqlalchemy import inspect, text

from app.db.session import get_engine, session_factory


def test_migrations_create_database(data_dir: Path) -> None:
    assert (data_dir / "app.db").exists()
    assert "alembic_version" in inspect(get_engine()).get_table_names()


def test_sqlite_foreign_keys_enabled(data_dir: Path) -> None:
    with session_factory()() as db:
        assert db.execute(text("PRAGMA foreign_keys")).scalar() == 1
