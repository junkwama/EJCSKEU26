# External modules
from sqlmodel import SQLModel
from pydantic import BaseModel, Field as PydanticField

# ---- CONTACT FIELDS CONFIG -----#
CONTACT_FIELDS_CONFIG = {
    "id_document_type": {
        "ge": 1,
        "le": 3,  # ✅ ADDED - validate range (1-3)
        "description": "Type de document (1=FIDELE, 2=PAROISSE, 3=STRUCTURE)",
    },
    "id_document": {
        "ge": 1,
        "description": "ID du document (fidele, paroisse, structure)",
    },
    "tel1": {
        "max_length": 20,
        "examples": ["+243812345678"],
        "description": "Téléphone principal",
    },
    "tel2": {
        "max_length": 20,
        "examples": ["+243812345679"],
        "description": "Téléphone secondaire (optionnel)",
    },
    "whatsapp": {
        "max_length": 20,
        "examples": ["+243812345680"],
        "description": "Numéro WhatsApp (optionnel)",
    },
    "email": {
        "max_length": 100,
        "examples": ["contact@example.com"],
        "description": "Email (optionnel)",
    },
}


# ---- CONTACT BASE MODEL -----#
class ContactBase(SQLModel):
    """Modèle de base pour créer un contact"""
    id_document_type: int = PydanticField(..., **CONTACT_FIELDS_CONFIG["id_document_type"], foreign_key="document_type.id")
    id_document: int = PydanticField(..., **CONTACT_FIELDS_CONFIG["id_document"])
    tel1: str = PydanticField(..., **CONTACT_FIELDS_CONFIG["tel1"])
    tel2: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["tel2"])
    whatsapp: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["whatsapp"])
    email: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["email"])


# ---- CONTACT UPDATE MODEL -----#
class ContactUpdate(BaseModel):
    """Modèle pour les mises à jour de contact (tous les champs optionnels)"""
    # ✅ REMOVED id_document_type and id_document - NOT editable
    tel1: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["tel1"])
    tel2: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["tel2"])
    whatsapp: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["whatsapp"])
    email: str | None = PydanticField(None, **CONTACT_FIELDS_CONFIG["email"])
