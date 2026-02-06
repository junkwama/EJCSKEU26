from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from models.adresse import Adresse
from models.contact import Contact
from models.fidele.utils import FideleBase
from models.constants import FideleType, Grade
from models.utils.utils import BaseModelClass

# Avoid circular dependency
if TYPE_CHECKING:
    from models.adresse import Adresse
    from models.contact import Contact

class Fidele(FideleBase, BaseModelClass, table=True):
    """Modèle de la table Fidele"""
    id_contact: int | None = Field(default=None, foreign_key="contact.id")
    id_adresse: int | None = Field(default=None, foreign_key="adresse.id")

    # Relationships
    grade: Grade | None = Relationship()
    fidele_type: FideleType | None = Relationship()
    contact: Contact | None = Relationship()
    adresse: Adresse | None = Relationship()