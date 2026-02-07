from sqlmodel import Relationship
from sqlalchemy import and_
from sqlalchemy.orm import relationship

from models.constants.types import DocumentTypeEnum
from utils.utils import SQLModelField
from models.adresse import Adresse
from models.contact import Contact
from models.fidele.utils import FideleBase
from models.constants import FideleType, Grade
from models.utils.utils import BaseModelClass


class Fidele(FideleBase, BaseModelClass, table=True):
    """Modèle de la table Fidele"""
    # OVERWRITTING TO AVOID ENUM TYPE ISSUES
    id_grade: int = SQLModelField(..., foreign_key="grade.id")
    id_fidele_type: int = SQLModelField(..., foreign_key="fidele_type.id")

    # Relationships
    grade: Grade = Relationship()
    fidele_type: FideleType = Relationship()
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

    class Config:
        from_attributes = True