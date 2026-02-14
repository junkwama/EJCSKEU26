from pydantic import BaseModel
from datetime import datetime
from typing import Union

from models.constants.projections import StructureProjShallow
from models.adresse.projection import ContinentProjFlat, NationProjFlat
from models.constants.projections import StructureProjFlat
from models.fidele.projection import FideleProjFlat
from models.paroisse.projection import ParoisseProjFlat

DirectionDocumentProj = Union[
    ParoisseProjFlat,
    NationProjFlat,
    ContinentProjFlat,
    StructureProjFlat,
    FideleProjFlat,
]


class DirectionProjFlat(BaseModel):
    id: int
    id_structure: int
    id_document_type: int
    id_document: int
    nom: str | None

    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class DirectionProjShallow(DirectionProjFlat):
    structure: StructureProjShallow
    document: DirectionDocumentProj | None = None

    class Config:
        from_attributes = True
