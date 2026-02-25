from typing import TYPE_CHECKING, List
from sqlalchemy import Index, UniqueConstraint
from sqlmodel import Relationship
from sqlalchemy import and_
from sqlalchemy.orm import relationship

from models.adresse import Adresse
from models.contact import Contact

from models.paroisse.utils import ParoisseBase
from models.utils.utils import BaseModelClass
from models.constants.types import DocumentTypeEnum

if TYPE_CHECKING:
    from models.fidele import FideleParoisse


class Paroisse(ParoisseBase, BaseModelClass, table=True):
    """Modèle de la table Paroisse - Paroisses"""

    __tablename__ = "paroisse"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_paroisse_nom"),
    )
    
    # Relationships
    fidele_paroisses: List["FideleParoisse"] | None = Relationship(back_populates="paroisse")
    contact: Contact | None = Relationship(
        sa_relationship=relationship(
            "Contact",
            primaryjoin=lambda: and_(
                Paroisse.id == Contact.id_document,
                Contact.id_document_type == DocumentTypeEnum.PAROISSE.value
            ),
            foreign_keys=lambda: [Contact.id_document, Contact.id_document_type],
            uselist=False
        ),
    )
    adresse: Adresse | None = Relationship(
        sa_relationship=relationship(
            "Adresse",
            primaryjoin=lambda: and_(
                Paroisse.id == Adresse.id_document,
                Adresse.id_document_type == DocumentTypeEnum.PAROISSE.value
            ),
            foreign_keys=lambda: [Adresse.id_document, Adresse.id_document_type],
            uselist=False
        ),
    )
    
    class Config:
        from_attributes = True
