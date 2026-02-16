from typing import List, Optional
from pydantic import BaseModel, computed_field
from datetime import date, datetime

from models.adresse.projection import AdresseProjShallow, NationProjFlat
from models.constants.projections import (
    FideleTypeProjFlat,
    GradeProjFlat,
    StructureProjFlat,
    NiveauEtudesProjFlat,
    ProfessionProjFlat,
)
from models.constants.types import FideleTypeEnum, GradeEnum
from models.contact.projection import ContactProjShallow
from utils.utils import PydanticField
from models.paroisse.projection import ParoisseProjFlat

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
    contact: ContactProjShallow | None = None
    adresse: AdresseProjShallow | None = None
    structures: List["FideleStructureProjShallow"] = []
    paroisses: List["FideleParoisseProjShallowWithoutFideleData"] = []
    bapteme: Optional["FideleBaptemeProjShallowWithoutFideleData"] = None
    famille: Optional["FideleFamilleProjFlat"] = None
    origine: Optional["FideleOrigineProjShallowWithoutFideleData"] = None
    occupation: Optional["FideleOccupationProjShallowWithoutFideleData"] = None
    
    class Config:
        from_attributes = True

## ============================================================================
## SUB DATA PROJECTIONS
## ============================================================================

class FideleStructureProjFlat(BaseModel):
    """Projection plate de FideleStructure - sans relations"""
    id: int
    id_fidele: int
    id_structure: int
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

class FideleStructureProjShallowWithoutStructureData(FideleStructureProjFlat):
    """Projection shallow de FideleStructure - Contenant Fidele"""
    fidele: FideleProjFlat

    class Config:
        from_attributes = True

class FideleStructureProjShallowWithoutFideleData(FideleStructureProjFlat):
    """Projection shallow de FideleStructure - Contenant Structure"""
    structure: StructureProjFlat

    class Config:
        from_attributes = True


class FideleParoisseProjFlat(BaseModel):
    """Projection plate de FideleParoisse - sans relations"""
    id: int
    id_fidele: int
    id_paroisse: int
    date_adhesion: date | None
    date_sortie: date | None
    est_actif: bool
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleParoisseProjShallow(FideleParoisseProjFlat):
    """Projection shallow de FideleParoisse - avec les relations Fidele et Paroisse"""
    fidele: FideleProjFlat
    paroisse: ParoisseProjFlat

    class Config:
        from_attributes = True


class FideleParoisseProjShallowWithoutParoisseData(FideleParoisseProjFlat):
    """Projection shallow de FideleParoisse - Contenant Fidele"""
    fidele: FideleProjFlat

    class Config:
        from_attributes = True


class FideleParoisseProjShallowWithoutFideleData(FideleParoisseProjFlat):
    """Projection shallow de FideleParoisse - Contenant Paroisse"""
    paroisse: ParoisseProjFlat

    class Config:
        from_attributes = True


class FideleBaptemeProjFlat(BaseModel):
    id: int
    id_fidele: int
    date_bapteme: date | None
    id_paroisse: int | None
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleBaptemeProjShallowWithoutFideleData(FideleBaptemeProjFlat):
    paroisse: ParoisseProjFlat | None = None

    class Config:
        from_attributes = True


class FideleFamilleProjFlat(BaseModel):
    id: int
    id_fidele: int
    nom_conjoint: str | None
    postnom_conjoint: str | None
    prenom_conjoint: str | None
    nombre_enfants: int | None
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleOrigineProjFlat(BaseModel):
    id: int
    id_fidele: int
    village: str | None
    groupement: str | None
    secteur: str | None
    territoire: str | None
    district: str | None
    province: str | None
    id_nation: int | None
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleOrigineProjShallowWithoutFideleData(FideleOrigineProjFlat):
    nation: NationProjFlat | None = None

    class Config:
        from_attributes = True


class FideleOccupationProjFlat(BaseModel):
    id: int
    id_fidele: int
    id_niveau_etude: int
    id_profession: int
    ecole_universite_employeur: str | None
    est_supprimee: bool
    date_suppression: datetime | None
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


class FideleOccupationProjShallowWithoutFideleData(FideleOccupationProjFlat):
    niveau_etude: NiveauEtudesProjFlat
    profession: ProfessionProjFlat

    class Config:
        from_attributes = True
