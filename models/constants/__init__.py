from models.utils.utils import BaseModelClass
from utils.utils import PydanticField


class DocumentType(BaseModelClass, table=True):
    """Modèle de la table DocumentType - Types de documents (FIDELE, PAROISSE, STRUCTURE)"""
    __tablename__ = "document_type"

    nom: str = PydanticField(
        ...,
        max_length=100,
        description="Nom du type de document (FIDELE, PAROISSE, STRUCTURE)"
    )

    class Config:
        from_attributes = True  

class Grade(BaseModelClass, table=True):
    """Modèle de la table GradeFidele"""
    nom: str = PydanticField(
        ..., 
        max_length=100,
        description="Nom du grade du fidele"
    )

    class Config:
        from_attributes = True

class FideleType(BaseModelClass, table=True):
    """Modèle de la table FideleType"""
    __tablename__ = "fidele_type"
    nom: str = PydanticField(
        ..., 
        max_length=100,
        description="Nom du type du fidele"
    )

    class Config:
        from_attributes = True