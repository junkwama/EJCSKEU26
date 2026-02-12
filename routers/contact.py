from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone

# Local modules
from core.db import get_session
from models.contact import Contact
from models.contact.utils import ContactBase, ContactUpdate
from models.contact.projection import ContactProjFlat
from models.constants import DocumentType
from routers.utils.http_utils import send200, send404
from routers.dependencies import check_resource_exists

# ============================================================================
# ROUTER SETUP
# ============================================================================
contact_router = APIRouter(tags=["Contact"])


async def contact_required(
    id: Annotated[int, Path(..., description="ID du contact")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Contact:
    """Get and validate Contact exists"""
    return await check_resource_exists(Contact, session, filters={"id": id})

async def get_contact_complete_data_by_id(id: int, session: AsyncSession) -> Contact:
    statement = select(Contact).where(
        (Contact.id == id) & 
        (Contact.est_supprimee == False)
    )
    result = await session.exec(statement)
    contact = result.first()
    
    return contact


# ============================================================================
# ENDPOINTS
# ============================================================================
@contact_router.post("")
async def create_contact(
    contact_data: ContactBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ContactProjFlat: 
    """
    Créer un nouveau contact

    Body: ContactBase (contient id_document_type, id_document et autres champs)
    """
    await check_resource_exists(
        DocumentType, session, filters={"id": int(contact_data.id_document_type)}
    )

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
    contact: Annotated[Contact, Depends(contact_required)],
) -> ContactProjFlat:
    """
    Récupérer un contact par son ID
    """
    contact = await get_contact_complete_data_by_id(id, session)
    
    if not contact:
        return send404(["query", "id"], "Contact non existant")

    return send200(ContactProjFlat.model_validate(contact))


@contact_router.put("/{id}")
async def update_contact(
    contact_data: ContactUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    contact: Annotated[Contact, Depends(contact_required)],
) -> ContactProjFlat:
    """
    Modifier un contact existant
    """
    # Update fields (exclude document identifiers - they shouldn't be changed)
    update_data = contact_data.model_dump(
        mode="json",
        exclude_unset=True,
        exclude={"id_document_type", "id_document"},
    )
    for field, value in update_data.items():
        setattr(contact, field, value)

    contact.date_modification = datetime.now(timezone.utc)

    session.add(contact)
    await session.commit()
    await session.refresh(contact)

    # Fetch the complete data with relations for the response for the Shallow Projection
    contact_complet_data = await get_contact_complete_data_by_id(contact.id, session)

    return send200(ContactProjFlat.model_validate(contact_complet_data))


@contact_router.delete("/{id}")
async def delete_contact(
    session: Annotated[AsyncSession, Depends(get_session)],
    contact: Annotated[Contact, Depends(contact_required)],
) -> ContactProjFlat:
    """
    Supprimer un contact (hard delete)
    """
    # save the contact data for the response before deleting
    contact_proj = ContactProjFlat.model_validate(contact)
    
    # Hard delete the contact
    session.delete(contact)
    await session.commit()

    return send200(contact_proj)
