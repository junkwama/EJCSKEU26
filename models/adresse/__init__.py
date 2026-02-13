# Local modules
from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
from sqlmodel import Relationship
from models.adresse.utils import AdresseBase
from models.utils.utils import BaseModelClass
from utils.utils import PydanticField, SQLModelField

class Continent(BaseModelClass, table=True):
    """Continent de base pour adresse projection"""
    __tablename__ = "continent"

    nom: str = PydanticField(..., max_length=100, description="Nom du continent")

    __table_args__ = (
        UniqueConstraint("nom", name="uq_continent_nom"),
    )

    class Config:
        from_attributes = True

class Nation(BaseModelClass, table=True):
    """Nation de base pour adresse projection"""
    __tablename__ = "nation"

    id_continent: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("continent.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    nom: str = PydanticField(..., max_length=100, description="Nom de la nation")

    __table_args__ = (
        UniqueConstraint("nom", name="uq_nation_nom"),
    )

    continent: Continent = Relationship()

    class Config:
        from_attributes = True

class Adresse(AdresseBase, BaseModelClass, table=True):
    """Modèle de la table Adresse - Addresses avec support multi-document"""

    __tablename__ = "adresse"

    # ovveriride to avoid enum type issues for mysql
    id_nation: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("nation.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    id_document_type: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("document_type.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )

    __table_args__ = (
        Index("idx_adresse_nation", "id_nation"),
        Index("idx_adresse_document", "id_document_type", "id_document"),
        Index("idx_adresse_est_supprimee", "est_supprimee"),
    )
    
    nation: Nation = Relationship()

    class Config:
        from_attributes = True
