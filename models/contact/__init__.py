# Local modules
from models.contact.utils import ContactBase
from models.utils.utils import BaseModelClass


class Contact(ContactBase, BaseModelClass, table=True):
    """Modèle de la table Contact - Contacts avec support multi-document"""
    pass
