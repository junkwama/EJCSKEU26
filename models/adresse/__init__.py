# Local modules
from sqlmodel import Relationship
from models.adresse.utils import AdresseBase
from models.utils.utils import BaseModelClass
from utils.utils import PydanticField, SQLModelField

class Continent(BaseModelClass, table=True):
    """Continent de base pour adresse projection"""
    nom: str = PydanticField(..., max_length=100, description="Nom du continent")
    class Config:
        from_attributes = True

class Nation(BaseModelClass, table=True):
    """Nation de base pour adresse projection"""
    id_continent: int = SQLModelField(..., foreign_key="continent.id")
    nom: str = PydanticField(..., max_length=100, description="Nom de la nation")

    continent: Continent = Relationship()

    class Config:
        from_attributes = True

class Adresse(AdresseBase, BaseModelClass, table=True):
    """Modèle de la table Adresse - Addresses avec support multi-document"""

    # ovveriride to avoid enum type issues for mysql
    id_nation: int = SQLModelField(..., foreign_key="nation.id")
    id_document_type: int = SQLModelField(..., foreign_key="document_type.id")
    
    nation: Nation = Relationship()

    class Config:
        from_attributes = True
