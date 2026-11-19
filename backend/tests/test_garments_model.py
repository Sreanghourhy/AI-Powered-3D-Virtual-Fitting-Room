from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.config import REPO_ROOT
from app.db.models import Garment
from app.db.seed import seed_garments
from app.db.session import session_factory


def test_seed_inserts_two_shirts_and_two_pants(data_dir: Path) -> None:
    with session_factory()() as db:
        assert seed_garments(db) == 4
        garments = db.scalars(select(Garment)).all()
        assert sorted(g.category for g in garments) == ["bottom", "bottom", "top", "top"]


def test_seed_is_idempotent(data_dir: Path) -> None:
    with session_factory()() as db:
        seed_garments(db)
        seed_garments(db)
        assert len(db.scalars(select(Garment)).all()) == 4


def test_only_top_and_bottom_allowed(data_dir: Path) -> None:
    with session_factory()() as db:
        db.add(
            Garment(
                id="dress-red",
                name="Dress",
                category="dress",
                model_url="/x.glb",
                thumbnail_url="/x.svg",
                source_author="x",
                source_license="x",
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()


def test_seed_thumbnails_exist_in_static(data_dir: Path) -> None:
    with session_factory()() as db:
        seed_garments(db)
        for garment in db.scalars(select(Garment)):
            assert (REPO_ROOT / "static" / garment.thumbnail_url.lstrip("/")).is_file()
