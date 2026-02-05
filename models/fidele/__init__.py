from sqlmodel import Field, Relationship

from models.fidele.utils import FideleBase, FideleType, Grade
from models.utils.utils import Adresse, BaseModelClass, Contact

class Fidele(FideleBase, BaseModelClass, table=True):
    """Modèle de la table Fidele"""
    id_contact: int | None = Field(default=None, foreign_key="contact.id")
    id_adresse: int | None = Field(default=None, foreign_key="adresse.id")

    # Relationships
    grade: Grade | None = Relationship()
    fidele_type: FideleType | None = Relationship()
    contact: Contact | None = Relationship()
    adresse: Adresse | None = Relationship()