from models.utils.utils import BaseModelClass
from models.constants.utils import (
    DocumentTypeBase, GradeBase, FideleTypeBase,
    MouvementAssociationBase, FonctionBase
)


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


class MouvementAssociation(MouvementAssociationBase, BaseModelClass, table=True):
    """Modèle de la table MouvementAssociation - Type d'association (chorale, scouts, ...)"""
    __tablename__ = "mouvement_association"

    class Config:
        from_attributes = True


class Fonction(FonctionBase, BaseModelClass, table=True):
    """Modèle de la table FonctionList - Catalogue des fonctions"""
    __tablename__ = "fonction_list"

    class Config:
        from_attributes = True