from typing import TYPE_CHECKING, List
from sqlmodel import Relationship
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField
from models.constants.utils import (
    DocumentTypeBase, GradeBase, FideleTypeBase,
    StructureBase, FonctionBase, StructureTypeBase
)

if TYPE_CHECKING:
    from models.fidele import FideleStructure

class DocumentType(DocumentTypeBase, BaseModelClass, table=True):
    """Modèle de la table DocumentType - Types de documents (FIDELE, PAROISSE, STRUCTURE)"""
    __tablename__ = "document_type"

    class Config:
        from_attributes = True  


class Grade(GradeBase, BaseModelClass, table=True):
    """Modèle de la table Grade"""
    
    class Config:
        from_attributes = True


class FideleType(FideleTypeBase, BaseModelClass, table=True):
    """Modèle de la table FideleType"""
    __tablename__ = "fidele_type"
    
    class Config:
        from_attributes = True


class StructureType(StructureTypeBase, BaseModelClass, table=True):
    """Modèle de la table StructureType - Types de structures (Mouvement, Association, Service)"""
    __tablename__ = "structure_type"

    class Config:
        from_attributes = True
        

class Structure(StructureBase, BaseModelClass, table=True):
    """Modèle de la table Structure - Types de structures (Mouvement, Association, Service)"""
    __tablename__ = "structure"

    id_structure_type: int = SQLModelField(..., foreign_key="structure_type.id")
    structure_type: StructureType = Relationship()
    
    # N-N relationship with Fidele through FideleStructure
    fideles: List["FideleStructure"] = Relationship(back_populates="structure")
    
    class Config:
        from_attributes = True
        
class Fonction(FonctionBase, BaseModelClass, table=True):
    """Modèle de la table FonctionList - Catalogue des fonctions"""
    __tablename__ = "fonction_list"

    class Config:
        from_attributes = True