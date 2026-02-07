# External moduls
from fastapi import APIRouter, Depends, Path, Query
from typing import Annotated, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from datetime import datetime, timezone

# Local modules
from core.config import Config
from models.constants.types import DocumentTypeEnum
from models.fidele import Fidele
from models.fidele.utils import FideleBase, FideleUpdate
from models.fidele.projection import FideleProjFlat, FideleProjShallow
from models.adresse import Adresse
from models.adresse.utils import AdresseUpdate
from models.adresse.projection import AdresseProjFlat, AdresseProjShallow
from models.contact import Contact
from models.contact.utils import ContactUpdate
from models.contact.projection import ContactProjFlat, ContactProjShallow
from core.db import get_session
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200, send404

fidele_router = APIRouter(tags=["Fidele"])

async def required_fidele(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Fidele:
    """Get and validate Fidele exists"""
    return await check_resource_exists(Fidele, id, session)


async def get_fidele_complete_data_by_id(id: int, session: AsyncSession) -> Fidele:
    statement = (
        select(Fidele)
        .where(Fidele.id == id)
        .options(
            selectinload(Fidele.grade),
            selectinload(Fidele.fidele_type),
            selectinload(Fidele.contact),
            selectinload(Fidele.adresse)
        )
    )
    result = await session.exec(statement)
    fidele = result.first()
    
    return fidele

@fidele_router.post("")
async def create_fidele(
    fidele_data: FideleBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleProjShallow:
    """
    Créer un nouveau fidele

    ARGS:
        fidele_data (FideleBase): Les données du fidele à créer
    """
    # Create new fidele instance
    new_fidele = Fidele(**fidele_data.model_dump(mode='json'))

    # Add to session and commit
    session.add(new_fidele)
    await session.commit()
    await session.refresh(new_fidele)

    # Return the created fidele
    return send200(FideleProjShallow.model_validate(new_fidele))


@fidele_router.get("")
async def get_fideles(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=Config.MAX_ITEMS_PER_PAGE)] = Config.MAX_ITEMS_PER_PAGE,
) -> List[FideleProjFlat]:
    """
    Recuperer la liste des fideles avec pagination
    """
    # Fetching main data
    statement = (
        select(Fidele)
        .where(Fidele.est_supprimee == False)
        .offset(offset)
        .limit(limit)
    )
    
    result = await session.exec(statement)
    fidele_list = result.all()

    # Returning the list
    return send200([
        FideleProjFlat.model_validate(fidele) 
        for fidele in fidele_list
    ])


@fidele_router.get("/{id}")
async def get_fidele(
    id: Annotated[int, Path(..., description="Fidele's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleProjShallow:
    """
    Recuperer un fidele par son Id avec ses relations

    ARGS:
        id (int): L'Id du fidele à récupérer
    """
    # Fetching the requested fidele WITH eager loading
    fidele = await get_fidele_complete_data_by_id(id, session)

    # If there's no matching fidele
    if not fidele:
        return send404(["body", "id"], "Fidele non existant")

    # Return the fidele as projection
    return send200(FideleProjShallow.model_validate(fidele))


@fidele_router.put("/{id}")
async def update_fidele(
    fidele_data: FideleUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleProjShallow:
    """
    Modifier un fidele existant

    ARGS:
        id (int): L'Id du fidele à modifier
        fidele_data (FideleUpdate): Les données mises à jour du fidele
    """

    # Update fields (only provided fields)
    update_data = fidele_data.model_dump(mode='json', exclude_unset=True)
    for field, value in update_data.items():
        setattr(fidele, field, value)
    
    # Update modification timestamp
    fidele.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(fidele)
    await session.commit()

    # Re-query with eager loads so relationships are available for projection
    fidele_complete_data = await get_fidele_complete_data_by_id(fidele.id, session)

    # Return the updated fidele with related objects already loaded
    return send200(FideleProjShallow.model_validate(fidele_complete_data))

@fidele_router.put("/{id}/restore")
async def restore_fidele(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)]
) -> FideleProjShallow:
    """
    Restaurer un fidele supprimé (soft delete)

    ARGS:
        id (int): L'Id du fidele à restaurer
    """

    # If already is deleted, retore
    if fidele.est_supprimee:

        fidele.est_supprimee = False
        fidele.date_suppression = None
        fidele.date_modification = datetime.now(timezone.utc)

        session.add(fidele)
        await session.commit()

    # Re-query with eager loads so relationships are available for projection
    fidele_complete_data = await get_fidele_complete_data_by_id(fidele.id, session)

    return send200(FideleProjShallow.model_validate(fidele_complete_data))

@fidele_router.delete("/{id}")
async def delete_fidele(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleProjFlat:
    """
    Soft delete un fidele (marquer comme supprimé)

    ARGS:
        id (int): L'Id du fidele à supprimer
    """

    # Soft delete
    fidele.est_supprimee = True
    fidele.date_suppression = datetime.now(timezone.utc)
    fidele.date_modification = datetime.now(timezone.utc)

    session.add(fidele)
    await session.commit()

    return send200(FideleProjFlat.model_validate(fidele))


# ========================== ADRESSE ENDPOINTS ==========================

@fidele_router.put("/{id}/adresse")
async def update_fidele_adresse(
    adresse_data: AdresseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)]
) -> AdresseProjShallow:
    """
    Modifier l'adresse associée à un fidele

    ARGS:
        id (int): L'Id du fidele
        adresse_data (AdresseUpdate): Les données mises à jour de l'adresse
    """
    
    # Query adresse by document type (FIDELE=1) and fidele id
    adresse_stmt = (
        select(Adresse).where(
            (Adresse.id_document_type == DocumentTypeEnum.FIDELE.value) & 
            (Adresse.id_document == fidele.id)
        ).options(selectinload(Adresse.nation))
    )
    
    adresse_result = await session.exec(adresse_stmt)
    adresse = adresse_result.first()
    
    if not adresse:
        # Create new adresse if not found
        new_adresse = Adresse(
            id_document_type=DocumentTypeEnum.FIDELE.value,
            id_document=fidele.id,
            **adresse_data.model_dump(mode='json', exclude_unset=True)
        )
        session.add(new_adresse)
        await session.commit()
        await session.refresh(new_adresse)
        return send200(AdresseProjShallow.model_validate(new_adresse))
    
    # Update fields (exclude document identifiers)
    update_data = adresse_data.model_dump(
        mode='json', 
        exclude_unset=True, 
        exclude={'id_document_type', 'id_document'}
    )
    for field, value in update_data.items():
        setattr(adresse, field, value)

    # maybe it was deleted so let's make sure to restore it if that's the case
    adresse.est_supprimee = False
    adresse.date_suppression = None
    
    # Update modification timestamp
    adresse.date_modification = datetime.now(timezone.utc)
    
    # Commit changes
    session.add(adresse)
    await session.commit()
    await session.refresh(adresse)
    
    # Return the updated adresse
    return send200(AdresseProjShallow.model_validate(adresse))


@fidele_router.delete("/{id}/adresse")
async def delete_fidele_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> AdresseProjFlat:
    """
    Supprimer l'adresse associée à un fidele (hard delete)

    ARGS:
        id (int): L'Id du fidele
    """

    # Query adresse by document type and fidele id
    adresse_stmt = select(Adresse).where(
        (Adresse.id_document_type == DocumentTypeEnum.FIDELE.value) & 
        (Adresse.id_document == fidele.id)
    ).options(selectinload(Adresse.nation))

    adresse_result = await session.exec(adresse_stmt)
    adresse = adresse_result.first()
    
    if not adresse:
        return send404(["query", "id"], "Adresse non trouvée pour ce fidele")
    
    # Convert to projection BEFORE deletion
    adresse_proj = AdresseProjFlat.model_validate(adresse)
    
    # Hard delete
    session.delete(adresse)
    await session.commit()
    
    return send200(adresse_proj)


# ========================== CONTACT ENDPOINTS ==========================

@fidele_router.put("/{id}/contact")
async def update_fidele_contact(
    contact_data: ContactUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> ContactProjShallow:
    """
    Modifier le contact associé à un fidele

    ARGS:
        id (int): L'Id du fidele
        contact_data (ContactUpdate): Les données mises à jour du contact
    """
    
    # Query contact by document type (FIDELE=1) and fidele id
    contact_stmt = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.FIDELE.value) & 
        (Contact.id_document == fidele.id)
    )
    contact_result = await session.exec(contact_stmt)
    contact = contact_result.first()
    
    if not contact:
        # Create new contact if not found
        new_contact = Contact(
            id_document_type=DocumentTypeEnum.FIDELE.value,
            id_document=fidele.id,
            **contact_data.model_dump(mode='json', exclude_unset=True)
        )
        session.add(new_contact)
        await session.commit()
        await session.refresh(new_contact)
        return send200(ContactProjShallow.model_validate(new_contact))
    
    # Update fields (exclude document identifiers)
    update_data = contact_data.model_dump(mode='json', exclude_unset=True, exclude={'id_document_type', 'id_document'})
    for field, value in update_data.items():
        setattr(contact, field, value)

    # maybe it was deleted so let's make sure to restore it if that's the case
    contact.est_supprimee = False
    contact.date_suppression = None
    
    # Update modification timestamp
    contact.date_modification = datetime.now(timezone.utc)
    
    # Commit changes
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    
    # Return the updated contact
    return send200(ContactProjShallow.model_validate(contact))


@fidele_router.delete("/{id}/contact")
async def delete_fidele_contact(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> ContactProjFlat:
    """
    Supprimer le contact associé à un fidele

    ARGS:
        id (int): L'Id du fidele
    """
    
    # Query contact by document type and fidele id
    contact_stmt = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.FIDELE.value) & 
        (Contact.id_document == fidele.id)
    )
    contact_result = await session.exec(contact_stmt)
    contact = contact_result.first()

    if not contact:
        return send404(["query", "id"], "Contact non trouvé pour ce fidele")

    contact_proj = ContactProjFlat.model_validate(contact)
    
    # Hard delete (NO await - delete is not async)
    session.delete(contact)
    await session.commit()
    
    return send200(contact_proj)
