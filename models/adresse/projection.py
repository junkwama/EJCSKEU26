from pydantic import BaseModel
from datetime import datetime


class ContinentProjFlat(BaseModel):
    """Projection plate de continent"""
    id: int
    nom: str

    class Config:
        from_attributes = True

class NationProjFlat(BaseModel):
    """Projection plate de nation"""
    id: int
    nom: str
    id_continent: int
    class Config:
        from_attributes = True

class NationProjShallow(NationProjFlat):
    """Projection de nation avec relations imbriquées (continent)"""
    continent: ContinentProjFlat | None = None

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

    class Config:
        from_attributes = True

class AdresseProjShallow(AdresseProjFlat):
    """Projection d'adresse avec relations imbriquées"""
    nation: NationProjShallow | None = None
    
