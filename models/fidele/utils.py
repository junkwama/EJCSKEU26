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
    "id_fidele_recenseur": {
        "examples": [2],
        "description": "L'id du fidèle recenseur (ayant recensé ou confirmé ce fidèle)."
    },
    "id_nation_nationalite": {
        "examples": [1],
        "description": "L'id de la nation représentant la nationalité du fidèle."
    },
    "id_etat_civile": {
        "examples": [1],
        "description": "L'id de l'état civile du fidèle."
    },
    "id_document_statut": {
        "examples": [1],
        "description": "L'id du statut de document du fidèle (ex: En attente, Validé)."
    },
    "code_matriculation": {
        "min_length": 10,
        "max_length": 10,
        "examples": ["CD00000001"],
        "description": "Code matriculation unique du fidèle (attribué après validation)."
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
    id_fidele_recenseur: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_fidele_recenseur"])
    id_nation_nationalite: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_nation_nationalite"])
    id_etat_civile: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_etat_civile"])
    id_document_statut: int = PydanticField(1, **FIDELE_FIELDS_CONFIG["id_document_statut"])
    code_matriculation: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["code_matriculation"])
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
    id_fidele_recenseur: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_fidele_recenseur"])
    id_nation_nationalite: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_nation_nationalite"])
    id_etat_civile: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_etat_civile"])
    id_document_statut: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_document_statut"])
    code_matriculation: str | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["code_matriculation"])


class FideleStatutUpdate(BaseModel):
    id_document_statut: int = PydanticField(..., **FIDELE_FIELDS_CONFIG["id_document_statut"])
    id_fidele_recenseur: int | None = PydanticField(None, **FIDELE_FIELDS_CONFIG["id_fidele_recenseur"])


class FideleStructureBase(SQLModel):
    pass

    class Config:
        from_attributes = True

class FideleStructureUpdate(BaseModel):
    pass

    class Config:
        from_attributes = True

class FideleStructureCreate(FideleStructureUpdate):
    id_structure: int = PydanticField(..., examples=[1], description="Identifiant de la structure.")


class FideleParoisseBase(SQLModel):
    date_adhesion: date | None = PydanticField(None, examples=["2023-01-01"], description="Date d'adhésion")
    date_sortie: date | None = PydanticField(None, examples=["2023-12-31"], description="Date de sortie")

    class Config:
        from_attributes = True


class FideleParoisseUpdate(BaseModel):
    date_adhesion: date | None = PydanticField(None, examples=["2023-01-01"], description="Date d'adhésion")
    date_sortie: date | None = PydanticField(None, examples=["2023-12-31"], description="Date de sortie")

    class Config:
        from_attributes = True


class FideleParoisseCreate(FideleParoisseUpdate):
    id_paroisse: int = PydanticField(..., examples=[1], description="Identifiant de la paroisse")


class FideleBaptemeBase(SQLModel):
    date_bapteme: date | None = PydanticField(None, examples=["2015-06-15"], description="Date de baptême")

    class Config:
        from_attributes = True


class FideleBaptemeCreate(BaseModel):
    date_bapteme: date | None = PydanticField(None, examples=["2015-06-15"], description="Date de baptême")
    id_paroisse: int | None = PydanticField(None, examples=[1], description="Paroisse du baptême")

    class Config:
        from_attributes = True


class FideleBaptemeUpdate(BaseModel):
    date_bapteme: date | None = PydanticField(None, examples=["2015-06-15"], description="Date de baptême")
    id_paroisse: int | None = PydanticField(None, examples=[1], description="Paroisse du baptême")

    class Config:
        from_attributes = True


class FideleFamilleBase(SQLModel):
    nom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Kasongo"], description="Nom du conjoint")
    postnom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Mbuyi"], description="Postnom du conjoint")
    prenom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Marie"], description="Prénom du conjoint")
    nombre_enfants: int | None = PydanticField(None, ge=0, examples=[3], description="Nombre d'enfants")

    class Config:
        from_attributes = True


class FideleFamilleCreate(BaseModel):
    nom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Kasongo"], description="Nom du conjoint")
    postnom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Mbuyi"], description="Postnom du conjoint")
    prenom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Marie"], description="Prénom du conjoint")
    nombre_enfants: int | None = PydanticField(None, ge=0, examples=[3], description="Nombre d'enfants")

    class Config:
        from_attributes = True


class FideleFamilleUpdate(BaseModel):
    nom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Kasongo"], description="Nom du conjoint")
    postnom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Mbuyi"], description="Postnom du conjoint")
    prenom_conjoint: str | None = PydanticField(None, max_length=100, examples=["Marie"], description="Prénom du conjoint")
    nombre_enfants: int | None = PydanticField(None, ge=0, examples=[3], description="Nombre d'enfants")

    class Config:
        from_attributes = True


class FideleOrigineBase(SQLModel):
    village: str | None = PydanticField(None, max_length=120, examples=["Kisantu"], description="Village d'origine")
    groupement: str | None = PydanticField(None, max_length=120, examples=["Ngidinga"], description="Groupement d'origine")
    secteur: str | None = PydanticField(None, max_length=120, examples=["Lukunga"], description="Secteur d'origine")
    territoire: str | None = PydanticField(None, max_length=120, examples=["Madimba"], description="Territoire d'origine")
    district: str | None = PydanticField(None, max_length=120, examples=["Mont-Amba"], description="District d'origine")
    province: str | None = PydanticField(None, max_length=120, examples=["Kongo Central"], description="Province d'origine")

    class Config:
        from_attributes = True


class FideleOrigineCreate(BaseModel):
    village: str | None = PydanticField(None, max_length=120, examples=["Kisantu"], description="Village d'origine")
    groupement: str | None = PydanticField(None, max_length=120, examples=["Ngidinga"], description="Groupement d'origine")
    secteur: str | None = PydanticField(None, max_length=120, examples=["Lukunga"], description="Secteur d'origine")
    territoire: str | None = PydanticField(None, max_length=120, examples=["Madimba"], description="Territoire d'origine")
    district: str | None = PydanticField(None, max_length=120, examples=["Mont-Amba"], description="District d'origine")
    province: str | None = PydanticField(None, max_length=120, examples=["Kongo Central"], description="Province d'origine")
    id_nation: int | None = PydanticField(None, examples=[1], description="Nation d'origine")

    class Config:
        from_attributes = True


class FideleOrigineUpdate(BaseModel):
    village: str | None = PydanticField(None, max_length=120, examples=["Kisantu"], description="Village d'origine")
    groupement: str | None = PydanticField(None, max_length=120, examples=["Ngidinga"], description="Groupement d'origine")
    secteur: str | None = PydanticField(None, max_length=120, examples=["Lukunga"], description="Secteur d'origine")
    territoire: str | None = PydanticField(None, max_length=120, examples=["Madimba"], description="Territoire d'origine")
    district: str | None = PydanticField(None, max_length=120, examples=["Mont-Amba"], description="District d'origine")
    province: str | None = PydanticField(None, max_length=120, examples=["Kongo Central"], description="Province d'origine")
    id_nation: int | None = PydanticField(None, examples=[1], description="Nation d'origine")

    class Config:
        from_attributes = True


class FideleOccupationBase(SQLModel):
    ecole_universite_employeur: str | None = PydanticField(
        None,
        max_length=150,
        examples=["Université de Kinshasa"],
        description="École, université ou employeur actuel",
    )

    class Config:
        from_attributes = True


class FideleOccupationCreate(BaseModel):
    id_niveau_etude: int = PydanticField(..., examples=[1], description="Niveau d'étude du fidèle")
    id_profession: int = PydanticField(..., examples=[1], description="Profession du fidèle")
    ecole_universite_employeur: str | None = PydanticField(
        None,
        max_length=150,
        examples=["Université de Kinshasa"],
        description="École, université ou employeur actuel",
    )

    class Config:
        from_attributes = True


class FideleOccupationUpdate(BaseModel):
    id_niveau_etude: int = PydanticField(..., examples=[1], description="Niveau d'étude du fidèle")
    id_profession: int = PydanticField(..., examples=[1], description="Profession du fidèle")
    ecole_universite_employeur: str | None = PydanticField(
        None,
        max_length=150,
        examples=["Université de Kinshasa"],
        description="École, université ou employeur actuel",
    )

    class Config:
        from_attributes = True