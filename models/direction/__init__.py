from sqlmodel import Relationship

from models.direction.utils import DirectionBase
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField

from models.constants import Structure


class Direction(DirectionBase, BaseModelClass, table=True):
    """Modèle de la table direction"""

    id_structure: int = SQLModelField(..., foreign_key="structure.id")
    id_document_type: int = SQLModelField(..., foreign_key="document_type.id")

    structure: Structure = Relationship()

    class Config:
        from_attributes = True
