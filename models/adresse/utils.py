# External modules
from sqlmodel import SQLModel
from pydantic import BaseModel

# Local modules
from models.constants.types import DocumentTypeEnum
from utils.utils import PydanticField

# ---- NATION FIELDS CONFIG -----#
NATION_FIELDS_CONFIG = {
    "id_continent": {
        "ge": 1,
        "description": "Identifiant du continent",
    },
    "nom": {
        "max_length": 100,
        "examples": ["République Démocratique du Congo"],
        "description": "Nom de la nation",
    },
    "iso_alpha_2": {
        "min_length": 2,
        "max_length": 2,
        "examples": ["CD"],
        "description": "Code ISO alpha-2 de la nation",
    },
}

# ---- NATION BASE MODEL -----#
class NationBase(SQLModel):
    """Modèle de base pour créer une nation"""
    id_continent: int = PydanticField(..., **NATION_FIELDS_CONFIG["id_continent"])
    nom: str = PydanticField(..., **NATION_FIELDS_CONFIG["nom"])
    iso_alpha_2: str = PydanticField(..., **NATION_FIELDS_CONFIG["iso_alpha_2"])

# ---- NATION UPDATE MODEL -----#
class NationUpdate(BaseModel):
    """Modèle pour les mises à jour de nation (tous les champs optionnels)"""
    id_continent: int | None = PydanticField(None, **NATION_FIELDS_CONFIG["id_continent"])
    nom: str | None = PydanticField(None, **NATION_FIELDS_CONFIG["nom"])
    iso_alpha_2: str | None = PydanticField(None, **NATION_FIELDS_CONFIG["iso_alpha_2"])

# ---- ADRESSE FIELDS CONFIG -----#
ADRESSE_FIELDS_CONFIG = {
    "id_document_type": {
        "ge": 1,
        "examples": [1],
        "description": "Type de document (1=FIDELE, 2=PAROISSE, 3=STRUCTURE)",
    },
    "id_document": {
        "ge": 1,
        "examples": [1],
        "description": "ID du document (fidele, paroisse, structure)",
    },
    "id_nation": {
        "ge": 1,
        "le": 231, # Nombre total de nations dans la base de données
        "examples": [170],
        "description": "Identifiant de la nation. Ex: 170 pour la RDC",
    },
    "province_etat": {
        "max_length": 100,
        "examples": ["Kasai"],
        "description": "Province ou état",
    },
    "ville": {
        "max_length": 100,
        "examples": ["Kinshasa"],
        "description": "Ville",
    },
    "commune": {
        "max_length": 100,
        "examples": ["Lukunga"],
        "description": "Commune (optionnel)",
    },
    "avenue": {
        "max_length": 100,
        "examples": ["Avenue Lumumba"],
        "description": "Avenue ou rue",
    },
    "numero": {
        "max_length": 50,
        "examples": ["123"],
        "description": "Numéro du bâtiment",
    },
    "adresse_complete": {
        "max_length": 500,
        "examples": ["123 Avenue Lumumba, Kinshasa, RDC"],
        "description": "Adresse complète (optionnel)",
    },
}


# ---- ADRESSE BASE MODEL -----#
class AdresseBase(SQLModel):
    """Modèle de base pour créer une adresse"""
    id_document_type: DocumentTypeEnum = PydanticField(..., **ADRESSE_FIELDS_CONFIG["id_document_type"])
    id_document: int = PydanticField(..., **ADRESSE_FIELDS_CONFIG["id_document"])
    id_nation: int = PydanticField(..., **ADRESSE_FIELDS_CONFIG["id_nation"])
    province_etat: str = PydanticField(..., **ADRESSE_FIELDS_CONFIG["province_etat"])
    ville: str = PydanticField(..., **ADRESSE_FIELDS_CONFIG["ville"])
    commune: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["commune"])
    avenue: str = PydanticField(..., **ADRESSE_FIELDS_CONFIG["avenue"])
    numero: str = PydanticField(..., **ADRESSE_FIELDS_CONFIG["numero"])
    adresse_complete: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["adresse_complete"])


# ---- ADRESSE UPDATE MODEL -----#
class AdresseUpdate(BaseModel):
    """Modèle pour les mises à jour d'adresse (tous les champs optionnels)"""
    id_nation: int | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["id_nation"])
    province_etat: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["province_etat"])
    ville: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["ville"])
    commune: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["commune"])
    avenue: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["avenue"])
    numero: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["numero"])
    adresse_complete: str | None = PydanticField(None, **ADRESSE_FIELDS_CONFIG["adresse_complete"])
