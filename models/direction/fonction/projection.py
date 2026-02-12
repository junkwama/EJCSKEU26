from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from models.constants.projections import FonctionProjFlat
from models.direction.projection import DirectionProjFlat
from models.fidele.projection import FideleProjFlat


class DirectionFonctionProjFlat(BaseModel):
    id: int
    id_direction: int
    id_fidele: int
    id_fonction: int

    date_debut: date
    date_fin: date | None

    est_actif: bool
    est_suspendu: bool

    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class DirectionFonctionProjShallow(DirectionFonctionProjFlat):
    direction: DirectionProjFlat
    fidele: FideleProjFlat
    fonction: FonctionProjFlat

    class Config:
        from_attributes = True


class DirectionFonctionProjShallowWithoutDirectionData(DirectionFonctionProjFlat):
    """Variant shallow sans la direction (utile sous /direction/{id})."""

    fidele: FideleProjFlat
    fonction: FonctionProjFlat

    class Config:
        from_attributes = True


class DirectionFonctionProjShallowWithoutFideleData(DirectionFonctionProjFlat):
    """Variant shallow sans le fidèle (utile sous /fidele/{id})."""

    direction: DirectionProjFlat
    fonction: FonctionProjFlat

    class Config:
        from_attributes = True
