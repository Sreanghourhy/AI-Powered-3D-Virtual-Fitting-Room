"""Run Alembic migrations from Python: ``python -m app.db.migrate``."""

from alembic.config import Config

from alembic import command
from app.core.config import BACKEND_DIR


def alembic_config() -> Config:
    return Config(str(BACKEND_DIR / "alembic.ini"))


def upgrade_to_head() -> None:
    command.upgrade(alembic_config(), "head")


if __name__ == "__main__":
    upgrade_to_head()
    print("Database is up to date.")
