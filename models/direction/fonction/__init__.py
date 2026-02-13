from __future__ import annotations

from sqlmodel import Relationship
from sqlalchemy import Column, ForeignKey, Index, Integer

from models.constants import Fonction
from models.direction import Direction
from models.direction.fonction.utils import DirectionFonctionBase
from models.fidele import Fidele
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField


class DirectionFonction(DirectionFonctionBase, BaseModelClass, table=True):
    """Mandat: un fidèle occupe une fonction dans une direction."""

    __tablename__ = "direction_fonction"

    id_direction: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("direction.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_fidele: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fidele.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    id_fonction: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("fonction_list.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )

    est_actif: bool = SQLModelField(default=True)

    __table_args__ = (
        Index("idx_direction_fonction_current", "id_direction", "est_actif"),
        Index("idx_direction_fonction_fidele", "id_fidele"),
        Index("idx_direction_fonction_est_supprimee", "est_supprimee"),
    )

    direction: Direction = Relationship()
    fidele: Fidele = Relationship()
    fonction: Fonction = Relationship()

    class Config:
        from_attributes = True
