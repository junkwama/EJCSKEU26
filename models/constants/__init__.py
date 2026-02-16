from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
from sqlmodel import Relationship
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField
from models.constants.utils import (
    DocumentTypeBase, GradeBase, FideleTypeBase,
    StructureBase, FonctionBase, StructureTypeBase,
    ProfessionBase, NiveauEtudesBase, EtatCivileBase,
    DocumentStatutBase,
)

if TYPE_CHECKING:
    from models.fidele import FideleStructure

class DocumentType(DocumentTypeBase, BaseModelClass, table=True):
    """Modèle de la table DocumentType - Types de documents (FIDELE, PAROISSE, STRUCTURE)"""
    __tablename__ = "document_type"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_document_type_nom"),
        UniqueConstraint("document_key", name="uq_document_type_key"),
    )

    class Config:
        from_attributes = True  


class DocumentStatut(DocumentStatutBase, BaseModelClass, table=True):
    """Modèle de la table DocumentStatut"""
    __tablename__ = "document_statut"

    id_document_type: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("document_type.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    __table_args__ = (
        UniqueConstraint("nom", "id_document_type", name="uq_document_statut_nom_doc_type"),
        Index("idx_document_statut_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True


class Grade(GradeBase, BaseModelClass, table=True):
    """Modèle de la table Grade"""

    __tablename__ = "grade"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_grade_nom"),
    )
    
    class Config:
        from_attributes = True


class FideleType(FideleTypeBase, BaseModelClass, table=True):
    """Modèle de la table FideleType"""
    __tablename__ = "fidele_type"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_fidele_type_nom"),
    )
    
    class Config:
        from_attributes = True


class Profession(ProfessionBase, BaseModelClass, table=True):
    """Modèle de la table Profession"""
    __tablename__ = "profession"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_profession_nom"),
        Index("idx_profession_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True


class NiveauEtudes(NiveauEtudesBase, BaseModelClass, table=True):
    """Modèle de la table NiveauEtudes"""
    __tablename__ = "niveau_etudes"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_niveau_etudes_nom"),
        Index("idx_niveau_etudes_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True


class EtatCivile(EtatCivileBase, BaseModelClass, table=True):
    """Modèle de la table EtatCivile"""
    __tablename__ = "etat_civile"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_etat_civile_nom"),
        Index("idx_etat_civile_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True


class StructureType(StructureTypeBase, BaseModelClass, table=True):
    """Modèle de la table StructureType - Types de structures (Mouvement, Association, Service)"""
    __tablename__ = "structure_type"

    __table_args__ = (
        UniqueConstraint("nom", name="uq_structure_type_nom"),
        Index("idx_structure_type_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True
        

class Structure(StructureBase, BaseModelClass, table=True):
    """Modèle de la table Structure - Types de structures (Mouvement, Association, Service)"""
    __tablename__ = "structure"

    id_structure_type: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("structure_type.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    structure_type: StructureType = Relationship()
    
    # N-N relationship with Fidele through FideleStructure
    fideles: List["FideleStructure"] = Relationship(back_populates="structure")

    __table_args__ = (
        Index("idx_structure_est_supprimee", "est_supprimee"),
    )
    
    class Config:
        from_attributes = True
        
class Fonction(FonctionBase, BaseModelClass, table=True):
    """Modèle de la table FonctionList - Catalogue des fonctions"""
    __tablename__ = "fonction_list"

    id_document_type: int | None = SQLModelField(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("document_type.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    __table_args__ = (
        Index("idx_fonction_list_est_supprimee", "est_supprimee"),
    )

    class Config:
        from_attributes = True