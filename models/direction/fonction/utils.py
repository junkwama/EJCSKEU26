from __future__ import annotations

from datetime import date

from pydantic import BaseModel
from sqlmodel import SQLModel

from utils.utils import PydanticField


DIRECTION_FONCTION_FIELDS_CONFIG = {
    "id_fidele": {
        "ge": 1,
        "examples": [1],
        "description": "ID du fidèle (fidele.id)",
    },
    "id_fonction": {
        "ge": 1,
        "examples": [1],
        "description": "ID de la fonction (fonction_list.id)",
    },
    "date_debut": {
        "examples": ["2025-01-01"],
        "description": "Date de début du mandat",
    },
    "date_fin": {
        "examples": ["2025-12-31"],
        "description": "Date de fin du mandat (optionnel)",
    },
    "est_suspendu": {
        "examples": [False],
        "description": "Mandat suspendu (non actif)",
    },
}


class DirectionFonctionBase(SQLModel):
    id_fidele: int = PydanticField(..., **DIRECTION_FONCTION_FIELDS_CONFIG["id_fidele"])
    id_fonction: int = PydanticField(..., **DIRECTION_FONCTION_FIELDS_CONFIG["id_fonction"])
    date_debut: date = PydanticField(..., **DIRECTION_FONCTION_FIELDS_CONFIG["date_debut"])
    date_fin: date | None = PydanticField(None, **DIRECTION_FONCTION_FIELDS_CONFIG["date_fin"])
    est_suspendu: bool = PydanticField(False, **DIRECTION_FONCTION_FIELDS_CONFIG["est_suspendu"])


class DirectionFonctionCreate(DirectionFonctionBase):
    pass


class DirectionFonctionUpdate(BaseModel):
    date_debut: date | None = PydanticField(None, **DIRECTION_FONCTION_FIELDS_CONFIG["date_debut"])
    date_fin: date | None = PydanticField(None, **DIRECTION_FONCTION_FIELDS_CONFIG["date_fin"])
    est_suspendu: bool | None = PydanticField(None, **DIRECTION_FONCTION_FIELDS_CONFIG["est_suspendu"])
