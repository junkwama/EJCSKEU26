# External modules
from sqlmodel import SQLModel
from datetime import date
from utils.utils import PydanticField, SQLModelField


# Local modules
from models.utils.utils import (
    PSW_FIELD_PROPS,
    BaseModelClass,
    Password,
    Gender
)

from utils.constants import Regex

class Grade(BaseModelClass, table=True):
    """Modèle de la table GradeFidele"""
    nom: str = PydanticField(
        ..., 
        max_length=100,
        description="Nom du grade du fidele"
    )

class FideleType(BaseModelClass, table=True):
    """Modèle de la table FideleType"""
    __tablename__ = "fidele_type"
    nom: str = PydanticField(
        ..., 
        max_length=100,
        description="Nom du type du fidele"
    )

# ---- USER BASE MODEL -----#
class FideleBase(SQLModel):
    nom: str = PydanticField(
        ...,
        max_length=100,
        min_length=2,
        examples=["Mulamba"],
        description="Nom du fidele",
    )
    postnom: str | None = PydanticField(
        None,
        max_length=100,
        min_length=2,
        examples=["Matwiudi"],
        description="Postnom du fidele",
    )
    prenom: str = PydanticField(
        ...,
        max_length=100,
        min_length=2,
        examples=["Jean Marc"],
        description="Prenom du fidele",
    )
    sexe: Gender = PydanticField(
        ...,
        examples=["M"],
        description="Sexe du fidele. M pour Masculin et F pour Féminin",
    )
    date_naissance: date = PydanticField(
        ...,
        examples=["1990-01-01"],
        description="Date de naissance du fidele."
    )
    numero_carte: str | None = PydanticField(
        None,
        examples=["123456"],
        description="Numéro de carte du fidele."
    )
    id_grade: int | None = SQLModelField(
        None,
        description="L'id du grade du fidele.",
        foreign_key="grade.id"
    )
    id_fidele_type: int | None = SQLModelField(
        None,
        description="L'id du type du fidele.",
        foreign_key="fidele_type.id"
    )
    tel: str = PydanticField(
        ...,
        pattern=Regex.PHONE.value,
        examples=["+243812345678"],
        description="Numero de téléphone au format international. Ex: +243812345678",
    )
    password: Password | None = PydanticField(None, **PSW_FIELD_PROPS)

# class FideleBasePswRequired(FideleBase):
#     password: Password = PydanticField(..., **PSW_FIELD_PROPS)
