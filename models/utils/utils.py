from sqlmodel import SQLModel
from pydantic_core.core_schema import no_info_after_validator_function
from datetime import datetime, timezone
from enum import Enum


from utils.utils import PydanticField, SQLModelField
from modules.oauth2.utils import password_context
from utils.constants import Regex

class BaseModelClass(SQLModel):
    """Schéma pour les tables de base avec des champs communs"""
    id: int | None = SQLModelField(default=None, primary_key=True)
    date_creation: datetime = PydanticField(
        ...,
        description="Date de création de l'entrée",
        default_factory=lambda: datetime.now(timezone.utc)
    )
    date_modification: datetime = PydanticField(
        ...,
        description="Date de dernière modification de l'entrée",
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Config:
        from_attributes = True


class Gender(Enum):
    M = "M"
    F = "F"

class Adresse(BaseModelClass, table=True):
    """Modèle de la table Adresse"""
    id_nation: int = SQLModelField(
        ...,
        ge=1,
        le=231,
        description="Identifiant de la nation. Ex 170 pour la RDC",
        foreign_key="nation.id"
    )
    province_etat: str = PydanticField(
        ...,
        max_length=100,
        description="Nom de la province ou État",
    )
    ville: str = PydanticField(
        ...,
        max_length=100,
        description="Nom de la ville",
    )
    commune: str | None = PydanticField(
        None,
        max_length=100,
        description="Nom de la commune ou district",
    )
    avenue: str = PydanticField(
        ...,
        max_length=100,
        description="Nom de l'avenue",
    )
    numero: str = PydanticField(
        ...,
        max_length=50,
        description="Numéro de la maison ou du bâtiment",
    )
    adresse_complete: str | None = PydanticField(
        None,
        max_length=500,
        description="L'adresse complète",
    )


class Contact(BaseModelClass, table=True):
    """Modèle de la table Contact"""
    
    tel1: str | None = PydanticField(
        None,
        pattern=Regex.PHONE.value,
        description="Téléphone principal",
    )
    tel2: str | None = PydanticField(
        None,
        pattern=Regex.PHONE.value,
        description="Téléphone secondaire",
    )
    whatsapp: str | None = PydanticField(
        None,
        pattern=Regex.PHONE.value,
        description="Numéro WhatsApp",
    )
    email: str | None = PydanticField(
        None,
        pattern=Regex.EMAIL.value,
        description="Adresse email",
    )


class Password(str):

    @classmethod
    def __get_pydantic_core_schema__(cls, _, handler):
        return no_info_after_validator_function(
            cls.validate,  # Use this class method for custom validation
            handler(str),  # But first validate it as a basic string
        )

    @classmethod
    def validate(cls, value: str) -> "Password":
        # If none don't do the checking to avoid callind methods on None
        if value == None:
            return value
        else:
            # Ensure at least one uppercase letter
            if not any(char.isupper() for char in value):
                raise ValueError("Le mot de passe doit contenir au moins une lettre majuscule.")
            # Ensure at least one lowercase letter
            if not any(char.islower() for char in value):
                raise ValueError("Le mot de passe doit contenir au moins une lettre minuscule.")
            # Ensure at least one digit
            if not any(char.isdigit() for char in value):
                raise ValueError("Le mot de passe doit contenir au moins un chiffre.")
            # Ensure at least one special character
            special_characters = "@$!%*?&"
            if not any(char in special_characters for char in value):
                raise ValueError(
                    f"Le mot de passe doit contenir au moins un caractère spécial : {special_characters}"
                )
            return value

    @classmethod
    def hash(cls, password: str | None):
        return password_context.hash(password) if password else None

    @classmethod
    def check(cls, plain: str, hashed: str | None):
        return password_context.verify(plain, hashed)


PSW_FIELD_PROPS = {
    "min_length": 8,
    "max_length": 64,
    "example": "Ag?1*nv67",
    "description": "Inclut 1 majuscule, 1 minuscule, un chiffre et un caractère spécial. Min 8 et Max 64",
}
