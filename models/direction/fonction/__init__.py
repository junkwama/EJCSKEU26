from __future__ import annotations

from sqlmodel import Relationship

from models.constants import Fonction
from models.direction import Direction
from models.direction.fonction.utils import DirectionFonctionBase
from models.fidele import Fidele
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField


class DirectionFonction(DirectionFonctionBase, BaseModelClass, table=True):
    """Mandat: un fidèle occupe une fonction dans une direction."""

    __tablename__ = "direction_fonction"

    id_direction: int = SQLModelField(..., foreign_key="direction.id")
    id_fidele: int = SQLModelField(..., foreign_key="fidele.id")
    id_fonction: int = SQLModelField(..., foreign_key="fonction_list.id")

    est_actif: bool = SQLModelField(default=True)

    direction: Direction = Relationship()
    fidele: Fidele = Relationship()
    fonction: Fonction = Relationship()

    class Config:
        from_attributes = True
