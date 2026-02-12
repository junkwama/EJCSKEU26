# Local modules
from models.contact.utils import ContactBase
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField


class Contact(ContactBase, BaseModelClass, table=True):
    """Modèle de la table Contact - Contacts avec support multi-document"""
    id_document_type: int = SQLModelField(..., foreign_key="document_type.id")
