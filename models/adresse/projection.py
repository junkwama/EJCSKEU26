from pydantic import BaseModel
from datetime import datetime

class NationProjFlat(BaseModel):
    """Projection plate de nation"""
    id: int
    nom: str
    class Config:
        from_attributes = True

class AdresseProjFlat(BaseModel):
    """Projection plate d'adresse (niveau public)"""
    id: int
    id_document_type: int
    id_document: int
    id_nation: int
    province_etat: str
    ville: str
    commune: str | None
    avenue: str
    numero: str
    adresse_complete: str | None
    date_creation: datetime
    date_modification: datetime

    model_config = {"from_attributes": True}

class AdresseProjShallow(AdresseProjFlat):
    """Projection d'adresse avec relations imbriquées"""
    nation: NationProjFlat | None = None
