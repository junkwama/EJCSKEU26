# External modules
from sqlmodel import SQLModel
from pydantic import BaseModel
from datetime import date
from models.constants.types import GradeEnum, FideleTypeEnum
from utils.utils import PydanticField

# Local modules
from models.utils.utils import (
    PSW_FIELD_PROPS,
    Password,
    Gender
)

from utils.constants import Regex

# ---- FIDELE FIELDS CONFIG -----#
FIDELE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "min_length": 2,
        "examples": ["Mulamba"],
        "description": "Nom du fidele",
    },
    "postnom": {
        "max_length": 100,
        "min_length": 2,
        "examples": ["Matwiudi"],
        "description": "Postnom du fidele",
    },
    "prenom": {
        "max_length": 100,
        "min_length": 2,
        "examples": ["Jean Marc"],
        "description": "Prenom du fidele",
    },
    "sexe": {
        "examples": ["M"],
        "description": "Sexe du fidele. M pour Masculin et F pour Féminin",
    },
    "date_naissance": {
        "examples": ["1990-01-01"],
        "description": "Date de naissance du fidele."
    },
    "est_baptise": {
        "description": "Indique si le fidèle est baptisé"
    },
    "date_bapteme": {
        "examples": ["2015-06-15"],
        "description": "Date de baptême du fidèle (optionnel si pas baptisé)"
    },
    "numero_carte": {
        "examples": ["123456"],
        "description": "Numéro de carte du fidele."
    },
    "id_grade": {
        "examples": [1, 2, 3],
        "description": "L'id du grade du fidele."
    },
    "id_fidele_type": {
        "examples": [1, 2, 3],
        "description": "L'id du type du fidele."
    },
    "id_paroisse": {
        "examples": [1, 2, 3],
        "description": "L'id de la paroisse du fidele."
    },
    "tel": {
        "pattern": Regex.PHONE.value,
        "examples": ["+243812345678"],
        "description": "Numero de téléphone au format international. Ex: +243812345678",
    }
}

# ---- USER BASE MODEL -----#
class FideleBase(SQLModel):
    nom: str = PydanticField(..., **FIDELE_FIELDS_CONFIG["nom"])
    postnom: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["postnom"])
    prenom: str = PydanticField(..., **FIDELE_FIELDS_CONFIG["prenom"])
    sexe: Gender = PydanticField(..., **FIDELE_FIELDS_CONFIG["sexe"])
    date_naissance: date = PydanticField(..., **FIDELE_FIELDS_CONFIG["date_naissance"])
    est_baptise: bool = PydanticField(..., **FIDELE_FIELDS_CONFIG["est_baptise"])
    date_bapteme: date | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["date_bapteme"])
    numero_carte: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["numero_carte"])
    id_grade: GradeEnum = PydanticField(..., **FIDELE_FIELDS_CONFIG["id_grade"])
    id_fidele_type: FideleTypeEnum = PydanticField(..., **FIDELE_FIELDS_CONFIG["id_fidele_type"])
    id_paroisse: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_paroisse"])
    tel: str = PydanticField(..., **FIDELE_FIELDS_CONFIG["tel"])
    password: Password | None = PydanticField(None, **PSW_FIELD_PROPS)

# ---- FIDELE UPDATE MODEL -----#
class FideleUpdate(BaseModel):
    """Modèle pour les mises à jour de fidele (tous les champs optionnels)"""
    nom: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["nom"])
    postnom: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["postnom"])
    prenom: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["prenom"])
    sexe: Gender | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["sexe"])
    date_naissance: date | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["date_naissance"])
    est_baptise: bool | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["est_baptise"])
    date_bapteme: date | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["date_bapteme"])
    numero_carte: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["numero_carte"])
    id_grade: GradeEnum | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_grade"])
    id_fidele_type: FideleTypeEnum | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_fidele_type"])
    id_paroisse: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_paroisse"])


class FideleStructureBase(SQLModel):
    id_fidele: int = PydanticField(...)
    id_structure: int = PydanticField(...)
    date_adhesion: date | None = PydanticField(None, examples=["2023-01-01"], description="Date d'adhésion")
    date_sortie: date | None = PydanticField(None, examples=["2023-12-31"], description="Date de sortie")

    class Config:
        from_attributes = True

class FideleStructureUpdate(BaseModel):
    date_adhesion: date | None = PydanticField(None, examples=["2023-01-01"], description="Date d'adhésion")
    date_sortie: date | None = PydanticField(None, examples=["2023-12-31"], description="Date de sortie")

    class Config:
        from_attributes = True

class FideleStructureCreate(FideleStructureUpdate):
    id_structure: int = PydanticField(..., examples=[1], description="Identifiant de la structure à laquelle le fidèle adhère")