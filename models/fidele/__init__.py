from typing import TYPE_CHECKING, List
from sqlmodel import Relationship
from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy import and_
from sqlalchemy.orm import relationship

from models.constants.types import DocumentTypeEnum
from utils.utils import SQLModelField
from models.adresse import Adresse
from models.contact import Contact
from modules.file.models import File
from models.fidele.utils import (
    FideleBase,
    FideleStructureBase,
    FideleParoisseBase,
    FideleBaptemeBase,
    FideleFamilleBase,
    FideleOrigineBase,
    FideleOccupationBase,
)
from models.constants import FideleType, Grade, Structure, Profession, NiveauEtudes, EtatCivile
from models.utils.utils import BaseModelClass

if TYPE_CHECKING:
    from models.adresse import Nation
    from models.paroisse import Paroisse

class Fidele(FideleBase, BaseModelClass, table=True):
    """Modèle de la table Fidele"""

    __tablename__ = "fidele"

    # OVERWRITTING TO AVOID ENUM TYPE ISSUES
    id_grade: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("grade.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    id_fidele_type: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele_type.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    id_fidele_recenseur: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    id_nation_nationalite: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("nation.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    id_etat_civile: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("etat_civile.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    __table_args__ = (
        UniqueConstraint("numero_carte", name="uq_fidele_numero_carte"),
        Index("idx_fidele_nom", "nom"),
        Index("idx_fidele_grade", "id_grade"),
        Index("idx_fidele_est_supprimee", "est_supprimee"),
    )

    # Relationships
    grade: Grade = Relationship()
    fidele_type: FideleType = Relationship()
    fidele_recenseur: "Fidele" = Relationship(
        sa_relationship=relationship(
            "Fidele",
            remote_side="Fidele.id",
            foreign_keys="Fidele.id_fidele_recenseur",
            uselist=False,
        )
    )
    nation_nationalite: "Nation" = Relationship()
    etat_civile: EtatCivile = Relationship()
    contact: Contact = Relationship(
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
    
    adresse: Adresse = Relationship(
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

    photo: File = Relationship(
        sa_relationship=relationship(
            "File",
            primaryjoin=lambda: and_(
                Fidele.id == File.id_document,
                File.id_document_type == DocumentTypeEnum.FIDELE.value
            ),
            foreign_keys=lambda: [File.id_document, File.id_document_type],
            uselist=False
        )
    )
    
    # N-N relationship with Structure through FideleStructure
    structures: List["FideleStructure"] = Relationship(back_populates="fidele")
    paroisses: List["FideleParoisse"] = Relationship(back_populates="fidele")
    bapteme: "FideleBapteme" = Relationship(back_populates="fidele")
    famille: "FideleFamille" = Relationship(back_populates="fidele")
    origine: "FideleOrigine" = Relationship(back_populates="fidele")
    occupation: "FideleOccupation" = Relationship(back_populates="fidele")

    class Config:
        from_attributes = True


class FideleStructure(FideleStructureBase,BaseModelClass,  table=True):
    """Modèle de la table FideleStructure - Table dell'Association entre fidele et structure"""
    __tablename__ = "fidele_structure"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_structure: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("structure.id", ondelete="CASCADE"),
            nullable=False,
        )
    )

    __table_args__ = (
        Index("idx_fidele_structure_fidele", "id_fidele"),
        Index("idx_fidele_structure_structure", "id_structure"),
        Index("idx_fidele_structure_est_supprimee", "est_supprimee"),
    )

    # Relationships
    fidele: Fidele = Relationship(back_populates="structures")
    structure: Structure = Relationship(back_populates="fideles")

    class Config:
        from_attributes = True


class FideleParoisse(FideleParoisseBase, BaseModelClass, table=True):
    """Historique d'appartenance d'un fidèle à des paroisses."""

    __tablename__ = "fidele_paroisse"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_paroisse: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("paroisse.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    est_actif: bool = SQLModelField(default=True)

    __table_args__ = (
        Index("idx_fidele_paroisse_fidele", "id_fidele"),
        Index("idx_fidele_paroisse_paroisse", "id_paroisse"),
        Index("idx_fidele_paroisse_est_supprimee", "est_supprimee"),
    )

    fidele: Fidele = Relationship(back_populates="paroisses")
    paroisse: "Paroisse" = Relationship(back_populates="fidele_paroisses")

    class Config:
        from_attributes = True


class FideleBapteme(FideleBaptemeBase, BaseModelClass, table=True):
    """Informations de baptême d'un fidèle."""

    __tablename__ = "fidele_bapteme"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_paroisse: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("paroisse.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    __table_args__ = (
        UniqueConstraint("id_fidele", name="uq_fidele_bapteme_fidele"),
        Index("idx_fidele_bapteme_fidele", "id_fidele"),
        Index("idx_fidele_bapteme_paroisse", "id_paroisse"),
        Index("idx_fidele_bapteme_est_supprimee", "est_supprimee"),
    )

    fidele: Fidele = Relationship(back_populates="bapteme")
    paroisse: "Paroisse" = Relationship()

    class Config:
        from_attributes = True


class FideleFamille(FideleFamilleBase, BaseModelClass, table=True):
    """Informations familiales d'un fidèle."""

    __tablename__ = "fidele_famille"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )

    __table_args__ = (
        UniqueConstraint("id_fidele", name="uq_fidele_famille_fidele"),
        Index("idx_fidele_famille_fidele", "id_fidele"),
        Index("idx_fidele_famille_est_supprimee", "est_supprimee"),
    )

    fidele: Fidele = Relationship(back_populates="famille")

    class Config:
        from_attributes = True


class FideleOrigine(FideleOrigineBase, BaseModelClass, table=True):
    """Informations sur le lieu d'origine d'un fidèle."""

    __tablename__ = "fidele_origine"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_nation: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("nation.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    __table_args__ = (
        UniqueConstraint("id_fidele", name="uq_fidele_origine_fidele"),
        Index("idx_fidele_origine_fidele", "id_fidele"),
        Index("idx_fidele_origine_nation", "id_nation"),
        Index("idx_fidele_origine_est_supprimee", "est_supprimee"),
    )

    fidele: Fidele = Relationship(back_populates="origine")
    nation: "Nation" = Relationship()

    class Config:
        from_attributes = True


class FideleOccupation(FideleOccupationBase, BaseModelClass, table=True):
    """Informations d'occupation (études/profession) d'un fidèle."""

    __tablename__ = "fidele_occupation"

    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_niveau_etude: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("niveau_etudes.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    id_profession: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("profession.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )

    __table_args__ = (
        UniqueConstraint("id_fidele", name="uq_fidele_occupation_fidele"),
        Index("idx_fidele_occupation_fidele", "id_fidele"),
        Index("idx_fidele_occupation_niveau", "id_niveau_etude"),
        Index("idx_fidele_occupation_profession", "id_profession"),
        Index("idx_fidele_occupation_est_supprimee", "est_supprimee"),
    )

    fidele: Fidele = Relationship(back_populates="occupation")
    niveau_etude: NiveauEtudes = Relationship()
    profession: Profession = Relationship()

    class Config:
        from_attributes = True