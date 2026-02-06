from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone

# Local modules
from core.db import get_session
from models.contact import Contact
from models.contact.utils import ContactBase, ContactUpdate
from models.contact.projection import ContactProjFlat, ContactProjShallow
from routers.utils.http_utils import send200, send404

# ============================================================================
# ROUTER SETUP
# ============================================================================
contact_router = APIRouter(tags=["Contact"])


# ============================================================================
# ENDPOINTS
# ============================================================================
@contact_router.post("")
async def create_contact(
    contact_data: ContactBase,
    session: Annotated[AsyncSession, Depends(get_session)],  # ✅ FIXED - no = None
) -> ContactProjFlat:  # ✅ FIXED - consistent return type
    """
    Créer un nouveau contact

    Body: ContactBase (contient id_document_type, id_document et autres champs)
    """
    # Create contact
    contact = Contact(**contact_data.model_dump(mode="json"))

    session.add(contact)
    await session.commit()
    await session.refresh(contact)

    return send200(ContactProjFlat.model_validate(contact))


@contact_router.get("/{id}")
async def get_contact(
    id: Annotated[int, Path(..., description="ID du contact")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ContactProjShallow:
    """
    Récupérer un contact par son ID
    """
    statement = select(Contact).where(Contact.id == id)
    result = await session.exec(statement)
    contact = result.first()

    if not contact:
        return send404(["query", "id"], "Contact non existant")

    return send200(ContactProjShallow.model_validate(contact))


@contact_router.put("/{id}")
async def update_contact(
    id: Annotated[int, Path(..., description="ID du contact")],
    contact_data: ContactUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ContactProjShallow:
    """
    Modifier un contact existant
    """
    statement = select(Contact).where(Contact.id == id)
    result = await session.exec(statement)
    contact = result.first()

    if not contact:
        return send404(["query", "id"], "Contact non existant")

    # Update fields (exclude document identifiers - they shouldn't be changed)
    update_data = contact_data.model_dump(
        mode="json",
        exclude_unset=True,
        exclude={"id_document_type", "id_document"},  # ✅ FIXED - exclude these
    )
    for field, value in update_data.items():
        setattr(contact, field, value)

    contact.date_modification = datetime.now(timezone.utc)

    session.add(contact)
    await session.commit()
    await session.refresh(contact)

    return send200(ContactProjShallow.model_validate(contact))


@contact_router.delete("/{id}")
async def delete_contact(
    id: Annotated[int, Path(..., description="ID du contact")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    """
    Supprimer un contact (hard delete)
    """
    statement = select(Contact).where(Contact.id == id)
    result = await session.exec(statement)
    contact = result.first()

    if not contact:
        return send404(["query", "id"], "Contact non existant")

    # ✅ Convert to projection BEFORE deletion
    contact_proj = ContactProjShallow.model_validate(contact)
    
    # Hard delete (NO await - delete is not async)
    session.delete(contact)
    await session.commit()

    return send200(contact_proj)
