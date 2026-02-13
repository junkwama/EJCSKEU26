from sqlmodel import SQLModel
from pydantic_core.core_schema import no_info_after_validator_function
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import text

from utils.utils import SQLModelField

from modules.oauth2.utils import password_context

class BaseModelClass(SQLModel):
    """Base class with soft delete support"""
    id: int | None = SQLModelField(default=None, primary_key=True)

    est_supprimee: bool = SQLModelField(
        default=False,
        nullable=False,
        sa_column_kwargs={"server_default": text("0")},
        description="Est supprimée (soft delete)",
    )

    date_suppression: Optional[datetime] = SQLModelField(
        default=None,
        nullable=True,
        description="Date de suppression logique",
    )

    date_creation: datetime = SQLModelField(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        description="Date de création",
    )

    date_modification: datetime = SQLModelField(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "server_onupdate": text("CURRENT_TIMESTAMP"),
        },
        description="Date de modification",
    )

    class Config:
        from_attributes = True


class Gender(Enum):
    M = "M"
    F = "F"

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
