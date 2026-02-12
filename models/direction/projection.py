from pydantic import BaseModel
from datetime import datetime

from models.constants.projections import StructureProjShallow


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

    class Config:
        from_attributes = True
