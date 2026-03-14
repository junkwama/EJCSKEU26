# Local modules
from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
from models.contact.utils import ContactBase
from models.utils.utils import BaseModelClass
from utils.utils import SQLModelField


class Contact(ContactBase, BaseModelClass, table=True):
    """Modèle de la table Contact - Contacts avec support multi-document"""
    __tablename__ = "contact"

    id_document_type: int = SQLModelField(
        sa_column=Column(
            Integer,
            ForeignKey("document_type.id", ondelete="RESTRICT"),
            nullable=False,
        )
    )

    __table_args__ = (
        UniqueConstraint("id_document_type", "id_document", name="uq_contact_document"),
        Index("idx_contact_document", "id_document_type", "id_document"),
        Index("idx_contact_est_supprimee", "est_supprimee"),
    )
