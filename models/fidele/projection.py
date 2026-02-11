from typing import List
from pydantic import BaseModel, computed_field
from datetime import date, datetime

from models.adresse.projection import AdresseProjShallow
from models.constants.projections import FideleTypeProjFlat, GradeProjFlat, StructureProjFlat
from models.constants.types import FideleTypeEnum, GradeEnum
from models.contact.projection import ContactProjShallow
from utils.utils import PydanticField
from models.paroisse import Paroisse

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
    est_baptise: bool = PydanticField(..., description="Est-ce que le fidèle est baptisé")
    date_bapteme: date | None = PydanticField(None, description="Date de baptême")
    
    @computed_field
    @property
    def age(self) -> int:
        """Âge calculé basé sur la date de naissance"""
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )

    id_grade: GradeEnum 
    id_fidele_type: FideleTypeEnum
    id_paroisse: int | None = None

    est_supprimee: bool
    date_suppression: datetime | None = None
    
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True

class FideleProjShallow(FideleProjFlat):
    """
    PUBLIC x SHALLOW PROJECTION
    Everything in PublicFlat + Flat versions of public related fields
    """
    # Flat versions of related fields (with their nested fields)
    grade: GradeProjFlat
    fidele_type: FideleTypeProjFlat
    paroisse: Paroisse | None = None
    contact: ContactProjShallow | None = None
    adresse: AdresseProjShallow | None = None
    structures: List["FideleStructureProjShallow"] = []
    
    class Config:
        from_attributes = True

## ============================================================================
## FIDELE-STRUCTURE PROJECTIONS
## ============================================================================

class FideleStructureProjFlat(BaseModel):
    """Projection plate de FideleStructure - sans relations"""
    id: int
    id_fidele: int
    id_structure: int
    date_adhesion: datetime | None
    date_sortie: datetime | None
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleStructureProjShallow(FideleStructureProjFlat):
    """Projection shallow de FideleStructure - avec les relations Fidele et Structure"""
    fidele: FideleProjFlat
    structure: StructureProjFlat

    class Config:
        from_attributes = True

class FideleStructureProjShallowWithFideleData(FideleStructureProjFlat):
    """Projection shallow de FideleStructure - Contenant Fidele"""
    fidele: FideleProjFlat

    class Config:
        from_attributes = True

class FideleStructureProjShallowWithStructureData(FideleStructureProjFlat):
    """Projection shallow de FideleStructure - Contenant Structure"""
    structure: StructureProjFlat

    class Config:
        from_attributes = True
