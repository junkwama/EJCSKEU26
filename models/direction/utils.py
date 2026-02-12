from sqlmodel import SQLModel
from pydantic import BaseModel

from utils.utils import PydanticField


DIRECTION_FIELDS_CONFIG = {
    "id_structure": {
        "ge": 1,
        "examples": [1],
        "description": "ID de la structure (structure.id)",
    },
    "id_document_type": {
        "ge": 1,
        "examples": [2],
        "description": "Type de document cible (document_type.id)",
    },
    "id_document": {
        "ge": 1,
        "examples": [1],
        "description": "ID du document cible (paroisse/fidele/...) selon id_document_type",
    },
    "nom": {
        "max_length": 255,
        "examples": ["Bureau paroissial - Paroisse Torino (Italie)"],
        "description": "Nom affiché de la direction (optionnel)",
    },
}


class DirectionBase(SQLModel):
    id_structure: int = PydanticField(..., **DIRECTION_FIELDS_CONFIG["id_structure"])
    id_document_type: int = PydanticField(..., **DIRECTION_FIELDS_CONFIG["id_document_type"])
    id_document: int = PydanticField(..., **DIRECTION_FIELDS_CONFIG["id_document"])
    nom: str | None = PydanticField(None, **DIRECTION_FIELDS_CONFIG["nom"])


class DirectionUpdate(BaseModel):
    id_structure: int | None = PydanticField(None, **DIRECTION_FIELDS_CONFIG["id_structure"])
    id_document_type: int | None = PydanticField(None, **DIRECTION_FIELDS_CONFIG["id_document_type"])
    id_document: int | None = PydanticField(None, **DIRECTION_FIELDS_CONFIG["id_document"])
    nom: str | None = PydanticField(None, **DIRECTION_FIELDS_CONFIG["nom"])
