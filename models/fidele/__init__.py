from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship
from sqlalchemy import and_
from sqlalchemy.orm import relationship

from models.constants.types import DocumentTypeEnum
from utils.utils import SQLModelField
from models.adresse import Adresse
from models.contact import Contact
from models.fidele.utils import FideleBase, FideleStructureBase
from models.constants import FideleType, Grade, Structure
from models.utils.utils import BaseModelClass

if TYPE_CHECKING:
    from models.paroisse import Paroisse

class Fidele(FideleBase, BaseModelClass, table=True):
    """Modèle de la table Fidele"""
    # OVERWRITTING TO AVOID ENUM TYPE ISSUES
    id_grade: int = SQLModelField(..., foreign_key="grade.id")
    id_fidele_type: int = SQLModelField(..., foreign_key="fidele_type.id")
    id_paroisse: int | None = SQLModelField(None, foreign_key="paroisse.id")

    # Relationships
    grade: Grade = Relationship()
    fidele_type: FideleType = Relationship()
    paroisse: Optional["Paroisse"] = Relationship(back_populates="fideles")
    contact: Contact | None = Relationship(
        sa_relationship=relationship(
            "Contact",
            primaryjoin=lambda: and_(
                Fidele.id == Contact.id_document,
                Contact.id_document_type == DocumentTypeEnum.FIDELE.value
            ),
            foreign_keys=lambda: [Contact.id_document, Contact.id_document_type],
            uselist=False
        )
    )
    
    adresse: Adresse | None = Relationship(
        sa_relationship=relationship(
            "Adresse",
            primaryjoin=lambda: and_(
                Fidele.id == Adresse.id_document,
                Adresse.id_document_type == DocumentTypeEnum.FIDELE.value
            ),
            foreign_keys=lambda: [Adresse.id_document, Adresse.id_document_type],
            uselist=False
        )
    )
    
    # N-N relationship with Structure through FideleStructure
    structures: List["FideleStructure"] = Relationship(back_populates="fidele")

    class Config:
        from_attributes = True


class FideleStructure(FideleStructureBase,BaseModelClass,  table=True):
    """Modèle de la table FideleStructure - Table dell'Association entre fidele et structure"""
    __tablename__ = "fidele_structure"

    id_fidele: int = SQLModelField(..., foreign_key="fidele.id")
    id_structure: int = SQLModelField(..., foreign_key="structure.id")

    # Relationships
    fidele: Fidele = Relationship(back_populates="structures")
    structure: Structure = Relationship(back_populates="fideles")

    class Config:
        from_attributes = True