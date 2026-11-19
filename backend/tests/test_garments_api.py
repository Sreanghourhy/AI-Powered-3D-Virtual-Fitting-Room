from fastapi.testclient import TestClient

from app.db.models import Garment
from app.db.seed import seed_garments
from app.db.session import session_factory


def _seed() -> None:
    with session_factory()() as db:
        seed_garments(db)


def test_list_all_garments_is_public(client: TestClient) -> None:
    _seed()
    response = client.get("/garments")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 4
    assert [g["category"] for g in items] == ["top", "top", "bottom", "bottom"]


def test_response_matches_typescript_shape(client: TestClient) -> None:
    _seed()
    item = client.get("/garments/shirt-basic-tee-white").json()
    assert set(item) == {
        "id", "name", "category", "modelUrl", "thumbnailUrl",
        "colors", "sizes", "source", "active",
    }  # fmt: skip
    assert set(item["source"]) == {"author", "license", "url"}


def test_filter_by_category(client: TestClient) -> None:
    _seed()
    tops = client.get("/garments", params={"category": "top"}).json()
    bottoms = client.get("/garments", params={"category": "bottom"}).json()
    assert {g["id"] for g in tops} == {"shirt-basic-tee-white", "shirt-oxford-blue"}
    assert {g["id"] for g in bottoms} == {"pants-chinos-beige", "pants-jeans-indigo"}


def test_unsupported_category_rejected(client: TestClient) -> None:
    assert client.get("/garments", params={"category": "dress"}).status_code == 422


def test_unknown_garment_404(client: TestClient) -> None:
    assert client.get("/garments/nope").status_code == 404


def test_inactive_garments_hidden(client: TestClient) -> None:
    _seed()
    with session_factory()() as db:
        db.get(Garment, "shirt-oxford-blue").active = False
        db.commit()
    ids = {g["id"] for g in client.get("/garments").json()}
    assert "shirt-oxford-blue" not in ids
    assert client.get("/garments/shirt-oxford-blue").status_code == 404
