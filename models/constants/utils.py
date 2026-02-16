from sqlmodel import SQLModel
from pydantic import BaseModel
from utils.utils import PydanticField

# ============================================================================
# DOCUMENT TYPE FIELDS CONFIG
# ============================================================================
DOCUMENT_TYPE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "description": "Nom du type de document (FIDELE, PAROISSE, STRUCTURE)"
    },
    "document_key": {
        "max_length": 50,
        "description": "Clé unique du type de document (ex: FIDELE, PAROISSE, STRUCTURE)"
    }
}


# ============================================================================
# GRADE FIELDS CONFIG
# ============================================================================
GRADE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "examples": ["Kengi"],
        "description": "Nom du grade ecclésiastique"
    }
}


# ============================================================================
# FIDELE TYPE FIELDS CONFIG
# ============================================================================
FIDELE_TYPE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "examples": ["Sympatisant"],
        "description": "Nom du type de fidèle"
    }
}


# ============================================================================
# PROFESSION FIELDS CONFIG
# ============================================================================
PROFESSION_FIELDS_CONFIG = {
    "nom": {
        "max_length": 150,
        "examples": ["Élève/Étudiant"],
        "description": "Nom de la profession",
    },
    "description": {
        "examples": ["Profession principale du fidèle"],
        "description": "Description de la profession (optionnelle)",
    },
}


# ============================================================================
# NIVEAU ETUDES FIELDS CONFIG
# ============================================================================
NIVEAU_ETUDES_FIELDS_CONFIG = {
    "nom": {
        "max_length": 150,
        "examples": ["Secondaire"],
        "description": "Niveau d'études",
    },
    "description": {
        "examples": ["Niveau d'études de base"],
        "description": "Description du niveau d'études (optionnelle)",
    },
}


# ============================================================================
# ETAT CIVILE FIELDS CONFIG
# ============================================================================
ETAT_CIVILE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "examples": ["Célibataire"],
        "description": "État civil",
    },
    "description": {
        "examples": ["Situation matrimoniale"],
        "description": "Description de l'état civil (optionnelle)",
    },
}


# ============================================================================
# STRUCTURE TYPE FIELDS CONFIG
# ============================================================================
STRUCTURE_TYPE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "examples": ["Mouvement"],
        "description": "Nom du type de structure (Mouvement, Association, Service)"
    }
}


# ============================================================================
# STRUCTURE FIELDS CONFIG
# ============================================================================
STRUCTURE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 255,
        "examples": ["Union de la Jeunesse Kimbanguiste"],
        "description": "Nom de la structure",
    },
    "code": {
        "max_length": 100,
        "examples": ["UJKI"],
        "description": "Code de la structure",
    },
    "description": {
        "examples": [
            "Union de la Jeunesse Kimbanguiste, mouvement de jeunesse de l'Eglise Kimbanguiste"
        ],
        "description": "Description de la structure",
    },
    "id_structure_type": {
        "ge": 1,
        "examples": [2],
        "description": "Type de structure (Mouvement, Association, Service)",
    },
}


# ============================================================================
# FONCTION FIELDS CONFIG
# ============================================================================
FONCTION_FIELDS_CONFIG = {
    "nom": {
        "max_length": 150,
        "examples": ["Président"],
        "description": "Nom de la fonction",
    },
    "description": {
        "examples": ["Président d'une structure"],
        "description": "Description de la fonction",
    },
    "ordre": {
        "ge": 0,
        "examples": [1],
        "description": "Ordre d'affichage de la fonction",
    },
    "id_document_type": {
        "ge": 1,
        "examples": [1],
        "description": "Type de document auquel s'applique cette fonction (optionnel)",
    },
}


# ============================================================================
# DOCUMENT TYPE BASE & UPDATE
# ============================================================================
class DocumentTypeBase(SQLModel):
    nom: str = PydanticField(..., **DOCUMENT_TYPE_FIELDS_CONFIG["nom"])
    document_key: str = PydanticField(..., **DOCUMENT_TYPE_FIELDS_CONFIG["document_key"])


class DocumentTypeUpdate(BaseModel):
    nom: str | None = PydanticField(None, **DOCUMENT_TYPE_FIELDS_CONFIG["nom"])
    document_key: str | None = PydanticField(None, **DOCUMENT_TYPE_FIELDS_CONFIG["document_key"])


# ============================================================================
# GRADE BASE & UPDATE
# ============================================================================
class GradeBase(SQLModel):
    nom: str = PydanticField(..., **GRADE_FIELDS_CONFIG["nom"])


class GradeUpdate(BaseModel):
    nom: str | None = PydanticField(None, **GRADE_FIELDS_CONFIG["nom"])


# ============================================================================
# FIDELE TYPE BASE & UPDATE
# ============================================================================
class FideleTypeBase(SQLModel):
    nom: str = PydanticField(..., **FIDELE_TYPE_FIELDS_CONFIG["nom"])


class FideleTypeUpdate(BaseModel):
    nom: str | None = PydanticField(None, **FIDELE_TYPE_FIELDS_CONFIG["nom"])


# ============================================================================
# PROFESSION BASE & UPDATE
# ============================================================================
class ProfessionBase(SQLModel):
    nom: str = PydanticField(..., **PROFESSION_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **PROFESSION_FIELDS_CONFIG["description"])


class ProfessionUpdate(BaseModel):
    nom: str | None = PydanticField(None, **PROFESSION_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **PROFESSION_FIELDS_CONFIG["description"])


# ============================================================================
# NIVEAU ETUDES BASE & UPDATE
# ============================================================================
class NiveauEtudesBase(SQLModel):
    nom: str = PydanticField(..., **NIVEAU_ETUDES_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **NIVEAU_ETUDES_FIELDS_CONFIG["description"])


class NiveauEtudesUpdate(BaseModel):
    nom: str | None = PydanticField(None, **NIVEAU_ETUDES_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **NIVEAU_ETUDES_FIELDS_CONFIG["description"])


# ============================================================================
# ETAT CIVILE BASE & UPDATE
# ============================================================================
class EtatCivileBase(SQLModel):
    nom: str = PydanticField(..., **ETAT_CIVILE_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **ETAT_CIVILE_FIELDS_CONFIG["description"])


class EtatCivileUpdate(BaseModel):
    nom: str | None = PydanticField(None, **ETAT_CIVILE_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **ETAT_CIVILE_FIELDS_CONFIG["description"])


# ============================================================================
# STRUCTURE TYPE BASE & UPDATE
# ============================================================================
class StructureTypeBase(SQLModel):
    nom: str = PydanticField(..., **STRUCTURE_TYPE_FIELDS_CONFIG["nom"])


class StructureTypeUpdate(BaseModel):
    nom: str | None = PydanticField(None, **STRUCTURE_TYPE_FIELDS_CONFIG["nom"])


# ============================================================================
# STRUCTURE BASE & UPDATE
# ============================================================================
class StructureBase(SQLModel):
    nom: str = PydanticField(..., **STRUCTURE_FIELDS_CONFIG["nom"])
    code: str | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["code"])
    description: str | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["description"])
    id_structure_type: int = PydanticField(..., **STRUCTURE_FIELDS_CONFIG["id_structure_type"])


class StructureUpdate(BaseModel):
    nom: str | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["nom"])
    code: str | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["code"])
    description: str | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["description"])
    id_structure_type: int | None = PydanticField(None, **STRUCTURE_FIELDS_CONFIG["id_structure_type"])


# ============================================================================
# FONCTION BASE & UPDATE
# ============================================================================
class FonctionBase(SQLModel):
    nom: str = PydanticField(..., **FONCTION_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["description"])
    ordre: int | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["ordre"])
    id_document_type: int | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["id_document_type"])


class FonctionUpdate(BaseModel):
    nom: str | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["nom"])
    description: str | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["description"])
    ordre: int | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["ordre"])
    id_document_type: int | None = PydanticField(None, **FONCTION_FIELDS_CONFIG["id_document_type"])
