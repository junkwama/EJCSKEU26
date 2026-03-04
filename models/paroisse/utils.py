from pydantic import BaseModel
from utils.utils import PydanticField

# ---- FIDELE FIELDS CONFIG -----#
FIDELE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "min_length": 2,
        "examples": ["Italie (Torino)"],
        "description": "Nom de la paroisse",
    },
}

class ParoisseBase(BaseModel):
    """Base Paroisse model with common fields"""
    nom: str = PydanticField(..., **FIDELE_FIELDS_CONFIG["nom"])

class ParoisseUpdate(ParoisseBase):
    """Model for updating a paroisse"""
    nom: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["nom"])

