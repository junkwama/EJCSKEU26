from pydantic import BaseModel, computed_field
from datetime import date, datetime

from models.utils.utils import Contact, Adresse
from utils.utils import PydanticField

class GradeBasic(BaseModel):
    """Basic projection of Grade"""
    id: int = PydanticField(..., description="Identifiant unique du grade")
    nom: str = PydanticField(..., description="Nom du grade du fidèle")

    class Config:
        from_attributes = True

class FideleTypeBasic(BaseModel):
    """Basic projection of FideleType"""
    id: int = PydanticField(..., description="Identifiant unique du type de fidèle")
    nom: str = PydanticField(..., description="Nom du type de fidèle")

    class Config:
        from_attributes = True

class FideleProjFlat(BaseModel):
    """
    PUBLIC x FLAT PROJECTION
    Public information + Basic versions of related fields
    Accessible by anyone (authenticated or not)
    """
    id: int = PydanticField(..., description="Identifiant unique du fidèle")
    numero_carte: str | None = None
    nom: str
    postnom: str | None = None
    prenom: str
    @computed_field
    @property
    def nom_complet(self) -> str:
        """Nom complet formaté"""
        if self.postnom:
            return f"{self.nom} {self.postnom} {self.prenom}"
        return f"{self.nom} {self.prenom}"
    
    sexe: str
    date_naissance: date
    @computed_field
    @property
    def age(self) -> int:
        """Âge calculé basé sur la date de naissance"""
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )
    
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True


class FideleProjShallow(FideleProjFlat):
    """
    PUBLIC x SHALLOW PROJECTION
    Everything in PublicFlat + Flat versions of public related fields
    """
    # Flat versions of related fields (with their nested fields)
    grade: GradeBasic | None = None
    fidele_type: FideleTypeBasic | None = None
    contact: Contact | None = None
    adresse: Adresse | None = None
