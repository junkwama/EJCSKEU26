from sqlmodel import Relationship
from sqlalchemy import Column, ForeignKey, Index, Integer

from models.direction.utils import DirectionBase
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField

from models.constants import Structure


class Direction(DirectionBase, BaseModelClass, table=True):
    """Modèle de la table direction"""

    id_structure: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("structure.id", ondelete="CASCADE"),
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
        Index("idx_direction_doc", "id_document_type", "id_document"),
        Index("idx_direction_structure", "id_structure"),
        Index("idx_direction_est_supprimee", "est_supprimee"),
    )

    structure: Structure = Relationship()

    class Config:
        from_attributes = True
