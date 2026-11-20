"""Shared test setup: every test gets a throwaway data directory, database and key."""

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

# Must be set before the app is imported.
os.environ["FR_ENVIRONMENT"] = "test"
os.environ["FR_DATA_DIR"] = tempfile.mkdtemp(prefix="fr-test-")
os.environ["FR_ENCRYPTION_KEY"] = "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY="
os.environ.pop("FR_DATABASE_URL", None)

from app.core.config import get_settings  # noqa: E402
from app.db.migrate import upgrade_to_head  # noqa: E402
from app.db.session import reset_engine  # noqa: E402


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Point the app at an empty, migrated database for this test only."""
    monkeypatch.setenv("FR_DATA_DIR", str(tmp_path))
    get_settings.cache_clear()
    reset_engine()
    upgrade_to_head()
    yield tmp_path
    reset_engine()
    get_settings.cache_clear()


@pytest.fixture
def client(data_dir: Path) -> Iterator["TestClient"]:
    """API client on a fresh database, talking to the app as http://localhost."""
    from fastapi.testclient import TestClient

    from app.main import create_app

    with TestClient(
        create_app(), base_url="http://localhost", headers={"X-Fitting-Room": "1"}
    ) as test_client:
        yield test_client
