from pydantic import BaseModel
from datetime import datetime

from models.adresse.projection import AdresseProjShallow
from models.contact.projection import ContactProjShallow

class ParoisseProjFlat(BaseModel):
    """
    PUBLIC x FLAT PROJECTION
    Basic paroisse information
    """
    id: int
    nom: str
    
    est_supprimee: bool
    date_suppression: datetime | None = None
    
    date_creation: datetime
    date_modification: datetime
    
    class Config:
        from_attributes = True


class ParoisseProjShallow(ParoisseProjFlat):
    """
    PUBLIC x SHALLOW PROJECTION
    Paroisse with basic nested relationships
    """
    contact: ContactProjShallow | None = None
    adresse: AdresseProjShallow | None = None
    
    class Config:
        from_attributes = True
