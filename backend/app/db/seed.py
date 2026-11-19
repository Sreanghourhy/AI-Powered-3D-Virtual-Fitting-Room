"""Seed the catalog with 2 shirts + 2 pants: ``python -m app.db.seed``.

Idempotent: re-running updates existing rows. Thumbnails are development placeholders;
GLB models are added in Phase 6 (docs/tasks/phase-6-try-on.md).
"""

from sqlalchemy.orm import Session

from app.db.models import Garment
from app.db.session import session_factory

PLACEHOLDER_SOURCE = {"source_author": "Project team", "source_license": "proprietary"}

SEED_GARMENTS: list[dict] = [
    {
        "id": "shirt-basic-tee-white",
        "name": "Basic Tee — White",
        "category": "top",
        "colors": ["#ffffff"],
        "sizes": ["S", "M", "L", "XL"],
        "sort_order": 10,
    },
    {
        "id": "shirt-oxford-blue",
        "name": "Oxford Shirt — Blue",
        "category": "top",
        "colors": ["#93c5fd"],
        "sizes": ["S", "M", "L", "XL"],
        "sort_order": 20,
    },
    {
        "id": "pants-chinos-beige",
        "name": "Chinos — Beige",
        "category": "bottom",
        "colors": ["#d6c4a1"],
        "sizes": ["28", "30", "32", "34", "36"],
        "sort_order": 10,
    },
    {
        "id": "pants-jeans-indigo",
        "name": "Jeans — Indigo",
        "category": "bottom",
        "colors": ["#3b4a7a"],
        "sizes": ["28", "30", "32", "34", "36"],
        "sort_order": 20,
    },
]


def seed_garments(db: Session) -> int:
    for item in SEED_GARMENTS:
        values = {
            **item,
            **PLACEHOLDER_SOURCE,
            "model_url": f"/garments/{item['id']}.glb",
            "thumbnail_url": f"/garments/{item['id']}.svg",
            "active": True,
        }
        garment = db.get(Garment, item["id"])
        if garment is None:
            db.add(Garment(**values))
        else:
            for key, value in values.items():
                setattr(garment, key, value)
    db.commit()
    return len(SEED_GARMENTS)


if __name__ == "__main__":
    with session_factory()() as session:
        print(f"Seeded {seed_garments(session)} garments.")
