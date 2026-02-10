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
    }
}


# ============================================================================
# GRADE FIELDS CONFIG
# ============================================================================
GRADE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "description": "Nom du grade ecclésiastique"
    }
}


# ============================================================================
# FIDELE TYPE FIELDS CONFIG
# ============================================================================
FIDELE_TYPE_FIELDS_CONFIG = {
    "nom": {
        "max_length": 100,
        "description": "Nom du type de fidèle"
    }
}


# ============================================================================
# MOUVEMENT ASSOCIATION FIELDS CONFIG
# ============================================================================
MOUVEMENT_ASSOCIATION_FIELDS_CONFIG = {
    "nom": {
        "max_length": 255,
        "description": "Nom du mouvement/association"
    },
    "code": {
        "max_length": 100,
        "description": "Code du mouvement/association"
    },
    "description": {
        "description": "Description du mouvement/association"
    }
}


# ============================================================================
# FONCTION FIELDS CONFIG
# ============================================================================
FONCTION_FIELDS_CONFIG = {
    "nom": {
        "max_length": 150,
        "description": "Nom de la fonction"
    },
    "description": {
        "description": "Description de la fonction"
    },
    "ordre": {
        "description": "Ordre d'affichage de la fonction"
    },
    "id_document_type": {
        "description": "Type de document auquel s'applique cette fonction (optionnel)"
    }
}


# ============================================================================
# DOCUMENT TYPE BASE & UPDATE
# ============================================================================
class DocumentTypeBase(SQLModel):
    nom: str = PydanticField(..., **DOCUMENT_TYPE_FIELDS_CONFIG["nom"])


class DocumentTypeUpdate(BaseModel):
    nom: str | None = PydanticField(None, **DOCUMENT_TYPE_FIELDS_CONFIG["nom"])


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
# MOUVEMENT ASSOCIATION BASE & UPDATE
# ============================================================================
class MouvementAssociationBase(SQLModel):
    nom: str = PydanticField(..., **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["nom"])
    code: str | None = PydanticField(None, **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["code"])
    description: str | None = PydanticField(None, **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["description"])


class MouvementAssociationUpdate(BaseModel):
    nom: str | None = PydanticField(None, **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["nom"])
    code: str | None = PydanticField(None, **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["code"])
    description: str | None = PydanticField(None, **MOUVEMENT_ASSOCIATION_FIELDS_CONFIG["description"])


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
