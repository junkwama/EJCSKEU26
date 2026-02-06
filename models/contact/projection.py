from pydantic import BaseModel
from datetime import datetime

class ContactProjFlat(BaseModel):
    """Projection plate de contact"""
    id: int
    id_document_type: int
    id_document: int
    tel1: str
    tel2: str | None
    whatsapp: str | None
    email: str | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class ContactProjShallow(ContactProjFlat):
    """Projection de contact avec relations (aucune relation actuellement)"""
    pass
