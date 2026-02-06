# Local modules
from sqlmodel import Relationship
from models.adresse.utils import AdresseBase
from models.utils.utils import BaseModelClass
from utils.utils import PydanticField

class Nation(BaseModelClass, table=True):
    """Nation de base pour adresse projection"""
    __tablename__ = "nation"
    
    nom: str = PydanticField(..., max_length=100, description="Nom de la nation")
    model_config = {"from_attributes": True}

class Adresse(AdresseBase, BaseModelClass, table=True):
    """Modèle de la table Adresse - Addresses avec support multi-document"""

    nation: Nation = Relationship()
