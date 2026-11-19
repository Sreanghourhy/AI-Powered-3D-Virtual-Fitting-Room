"""Public garment catalog (shirts and pants)."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DbSession
from app.api.schemas import GarmentCategory, GarmentOut
from app.db.models import Garment

router = APIRouter(prefix="/garments", tags=["catalog"])


@router.get("", response_model=list[GarmentOut])
def list_garments(db: DbSession, category: GarmentCategory | None = None) -> list[GarmentOut]:
    query = select(Garment).where(Garment.active.is_(True))
    if category:
        query = query.where(Garment.category == category)
    query = query.order_by(Garment.category.desc(), Garment.sort_order, Garment.name)
    return [GarmentOut.from_model(g) for g in db.scalars(query)]


@router.get("/{garment_id}", response_model=GarmentOut)
def get_garment(garment_id: str, db: DbSession) -> GarmentOut:
    garment = db.get(Garment, garment_id)
    if garment is None or not garment.active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Garment not found")
    return GarmentOut.from_model(garment)
