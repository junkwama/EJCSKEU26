# External moduls
from fastapi import APIRouter, Depends, Path, Query
from typing import Annotated, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from datetime import datetime, timezone

# Local modules
from core.config import Config
from core.db import get_session

from models.paroisse import Paroisse
from models.paroisse.utils import ParoisseBase, ParoisseUpdate
from models.paroisse.projection import ParoisseProjFlat, ParoisseProjShallow

from models.adresse import Adresse, Nation
from models.adresse.utils import AdresseUpdate
from models.adresse.projection import AdresseProjFlat, AdresseProjShallow

from models.contact import Contact
from models.contact.utils import ContactUpdate
from models.contact.projection import ContactProjFlat, ContactProjShallow

from utils.constants import ProjDepth
from models.constants.types import DocumentTypeEnum
from models.constants import DocumentType

from routers.dependencies import check_resource_exists
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send404

# ============================================================================
# ROUTER SETUP
# ============================================================================
paroisse_router = APIRouter()


async def get_paroisse_any_by_id(paroisse_id: int, session: AsyncSession) -> Paroisse | None:
    statement = select(Paroisse).where(Paroisse.id == paroisse_id)
    result = await session.exec(statement)
    return result.first()

async def required_paroisse(
    id: Annotated[int, Path(..., description="Paroisse's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Paroisse:
    """Get and validate Paroisse exists"""
    return await check_resource_exists(Paroisse, session, filters={"id": id})


async def get_paroisse_complete_data_by_id(
    id: int, session: AsyncSession, proj: ProjDepth = ProjDepth.SHALLOW
) -> Paroisse:
    statement = select(Paroisse).where(Paroisse.id == id)
    if proj == ProjDepth.SHALLOW:
            statement = statement.options(
            selectinload(Paroisse.contact),
            (
                selectinload(Paroisse.adresse)
                .selectinload(Adresse.nation)
                .selectinload(Nation.continent)
            )
        )

    result = await session.exec(statement)
    return result.first()

async def get_paroisse_adresse_complete_data_by_id(
    paroisse_id: int, session: AsyncSession, proj: ProjDepth = ProjDepth.SHALLOW
) -> Adresse:
    statement = (
        select(Adresse)
        .where(
            (Adresse.id_document_type == DocumentTypeEnum.PAROISSE.value)
            & (Adresse.id_document == paroisse_id)
            & (Adresse.est_supprimee == False)
        )
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Adresse.nation).selectinload(Nation.continent)
        )

    result = await session.exec(statement)
    return result.first()


# ============================================================================
# ENDPOINTS
# ============================================================================
@paroisse_router.post("", tags=["Paroisse"])
async def create_paroisse(
    body: ParoisseBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ParoisseProjFlat | ParoisseProjShallow:
    """
    Créer une nouvelle paroisse

    ARGS:
        body (ParoisseBase): Les données de la paroisse à créer
        proj (str): Projection type 'flat' or 'shallow' (default: shallow)
    """
    # Create new paroisse instance
    paroisse = Paroisse(**body.model_dump(mode='json'))

    # Add to session and commit
    session.add(paroisse)
    await session.commit()
    await session.refresh(paroisse)
    if proj == ProjDepth.SHALLOW:
        paroisse = await get_paroisse_complete_data_by_id(paroisse.id, session, proj)

    # Return the created paroisse
    projected_response = apply_projection(paroisse, ParoisseProjFlat, ParoisseProjShallow, proj)
    return send200(projected_response)


@paroisse_router.get("", tags=["Paroisse"])
async def get_paroisses(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(Config.PREVIEW_LIST_ITEM_NUMBER, ge=1, le=Config.MAX_ITEMS_PER_PAGE),
) -> List[ParoisseProjFlat | ParoisseProjShallow]:
    """
    Recuperer la liste des paroisses avec pagination
    
    Query:
        proj (str): Projection type 'flat' or 'shallow' (default: shallow)
        offset (int): Offset pour la pagination
        limit (int): Nombre maximum d'éléments à retourner
    """
    
    # Fetching main data
    statement = (
        select(Paroisse)
        .where(Paroisse.est_supprimee == False)
        .offset(offset)
        .limit(limit)
    )

    result = await session.exec(statement)
    paroisse_list = result.all()
    projected_paroisse_list = [ParoisseProjFlat.model_validate(paroisse) for paroisse in paroisse_list]

    # Returning the list
    return send200(projected_paroisse_list)


@paroisse_router.get("/{id}", tags=["Paroisse"])
async def get_paroisse(
    id: Annotated[int, Path(..., description="Paroisse's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ParoisseProjFlat | ParoisseProjShallow:
    """
    Recuperer une paroisse par son Id

    ARGS:
        id (int): L'Id de la paroisse à récupérer
        proj (str): Projection type 'flat' or 'shallow' (default: shallow)
    """

    # Fetching related data for the shallow projection
    if proj == ProjDepth.SHALLOW:
        paroisse = await get_paroisse_complete_data_by_id(id, session, proj)

    # Return the fidele as projection
    projected_response = apply_projection(paroisse, ParoisseProjFlat, ParoisseProjShallow, proj)
    return send200(projected_response)


@paroisse_router.put("/{id}", tags=["Paroisse"])
async def update_paroisse(
    body: ParoisseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ParoisseProjFlat | ParoisseProjShallow:
    """
    Modifier une paroisse existante

    ARGS:
        id (int): L'Id de la paroisse à modifier
        body (ParoisseUpdate): Les données mises à jour de la paroisse
        proj (str): Projection type 'flat' or 'shallow' (default: shallow)
    """
    # Update fields (only provided fields)
    update_data = body.model_dump(mode='json', exclude_unset=True)
    for field, value in update_data.items():
        setattr(paroisse, field, value)
    
    # Update modification timestamp
    paroisse.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(paroisse)
    await session.commit()
    await session.refresh(paroisse)

    # re-fetch to get related data for the shallow projection
    if proj == ProjDepth.SHALLOW:
        paroisse = await get_paroisse_complete_data_by_id(paroisse.id, session, proj)

    # Return the updated paroisse with requested projection
    projected_response = apply_projection(paroisse, ParoisseProjFlat, ParoisseProjShallow, proj)
    return send200(projected_response)

@paroisse_router.put("/{id}/restore", tags=["Paroisse"])
async def restore_paroisse(
    id: Annotated[int, Path(..., description="Paroisse's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ParoisseProjShallow | ParoisseProjFlat:
    """
    Restaurer une paroisse supprimée (soft deleted)

    ARGS:
        id (int): L'Id de la paroisse à restaurer
    """

    paroisse = await get_paroisse_any_by_id(id, session)
    if not paroisse:
        return send404(["path", "id"], "Paroisse non trouvée")

    # If already is deleted, restore
    if paroisse.est_supprimee:
        paroisse.est_supprimee = False
        paroisse.date_suppression = None
        paroisse.date_modification = datetime.now(timezone.utc)

        session.add(paroisse)
        await session.commit()

    # Re-query with eager loads so relationships are available for projection
    if proj == ProjDepth.SHALLOW:
        paroisse = await get_paroisse_complete_data_by_id(paroisse.id, session, proj)

    projected_response = apply_projection(paroisse, ParoisseProjFlat, ParoisseProjShallow, proj)
    return send200(projected_response)




@paroisse_router.delete("/{id}", tags=["Paroisse"])
async def delete_paroisse(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
) -> ParoisseProjFlat:
    """
    Soft delete une paroisse (marquer comme supprimée)

    ARGS:
        id (int): L'Id de la paroisse à supprimer
    """
    # Soft delete
    paroisse.est_supprimee = True
    paroisse.date_suppression = datetime.now(timezone.utc)
    paroisse.date_modification = datetime.now(timezone.utc)
 
    session.add(paroisse)
    await session.commit()

    projected_paroisse = ParoisseProjFlat.model_validate(paroisse)
    return send200(projected_paroisse)


# ============================================================================
# ADRESSE ENDPOINTS
# ============================================================================

@paroisse_router.get("/{id}/adresse", tags=["Paroisse - Adresse"])
async def get_paroisse_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Récupérer l'adresse associée à une paroisse

    ARGS:
        id (int): L'Id de la paroisse
    """

    # Query adresse by document type (PAROISSE=3) and paroisse id
    adresse = await get_paroisse_adresse_complete_data_by_id(paroisse.id, session, proj)

    if not adresse:
        return send404(["query", "id"], "Adresse non trouvée pour cette paroisse")

    projected_response = apply_projection(adresse, AdresseProjFlat, AdresseProjShallow, proj)
    return send200(projected_response)


@paroisse_router.put("/{id}/adresse", tags=["Paroisse - Adresse"])
async def update_paroisse_adresse(
    body: AdresseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ParoisseProjShallow | ParoisseProjFlat:
    """
    Modifier l'adresse associée à un fidele

    ARGS:
        id (int): L'Id du fidele
        body (AdresseUpdate): Les données mises à jour de l'adresse
    """

    # Query adresse by document type (PAROISSE=3) and paroisse id
    adresse = await get_paroisse_adresse_complete_data_by_id(paroisse.id, session, proj)

    if not adresse:
        if body.id_nation is not None:
            await check_resource_exists(Nation, session, filters={"id": body.id_nation})
        await check_resource_exists(
            DocumentType, session, filters={"id": DocumentTypeEnum.PAROISSE.value}
        )
        # Create new adresse if not found
        new_adresse = Adresse(
            id_document_type=DocumentTypeEnum.PAROISSE.value,
            id_document=paroisse.id,
            **body.model_dump(mode="json", exclude_unset=True)
        )
        session.add(new_adresse)
        await session.commit()
        await session.refresh(new_adresse)

        if proj == ProjDepth.SHALLOW:
            new_adresse = await get_paroisse_adresse_complete_data_by_id(paroisse.id, session, proj)

        projected_response = apply_projection(new_adresse, AdresseProjFlat, AdresseProjShallow, proj)
        return send200(projected_response)

    # Update fields (exclude document identifiers)
    update_data = body.model_dump(mode="json", exclude_unset=True, exclude={"id_document_type", "id_document"})
    if "id_nation" in update_data and update_data["id_nation"] is not None:
        await check_resource_exists(Nation, session, filters={"id": update_data["id_nation"]})
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
    projected_response = apply_projection(adresse, AdresseProjFlat, AdresseProjShallow, proj)
    return send200(projected_response)


@paroisse_router.delete("/{id}/adresse", tags=["Paroisse - Adresse"])
async def delete_paroisse_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
) -> AdresseProjFlat:
    """
    Supprimer l'adresse associée à un fidele (hard delete)

    ARGS:
        id (int): L'Id du fidele
    """

    # Query adresse
    adresse = await get_paroisse_adresse_complete_data_by_id(paroisse.id, session, ProjDepth.FLAT)

    if not adresse:
        return send404(["query", "id"], "Adresse non trouvée pour cette paroisse")

    # save in a projection before deletion for future access
    adresse_proj = AdresseProjFlat.model_validate(adresse)

    # Hard delete
    session.delete(adresse)
    await session.commit()

    return send200(adresse_proj)

# ============================================================================
# CONTACT ENDPOINTS
# ============================================================================

@paroisse_router.get("/{id}/contact", tags=["Paroisse - Contact"])
async def get_paroisse_contact(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ContactProjShallow | ContactProjFlat:
    """
    Récupérer le contact associée à un paroisse

    ARGS:
        id (int): L'Id du paroisse
    """
    # Query contact by document type (PAROISSE=3) and paroisse id
    statement = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.PAROISSE.value)
        & (Contact.id_document == paroisse.id)
    )
    contact_result = await session.exec(statement)
    contact = contact_result.first()

    if not contact:
        return send404(["query", "id"], "Contact non trouvé pour ce paroisse")
    projected_response = apply_projection(contact, ContactProjFlat, ContactProjShallow, proj)
    return send200(projected_response)


@paroisse_router.put("/{id}/contact", tags=["Paroisse - Contact"])
async def update_paroisse_contact(
    body: ContactUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ContactProjShallow | ContactProjFlat:
    """
    Modifier le contact associé à un paroisse

    ARGS:
        id (int): L'Id du paroisse
        body (ContactUpdate): Les données mises à jour du contact
    """

    # Query contact by document type (PAROISSE=3) and paroisse id
    statement = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.PAROISSE.value)
        & (Contact.id_document == paroisse.id)
        & (Contact.est_supprimee == False)
    )
    contact_result = await session.exec(statement)
    contact = contact_result.first()

    if not contact:
        await check_resource_exists(
            DocumentType, session, filters={"id": DocumentTypeEnum.PAROISSE.value}
        )
        # Create new contact if not found
        new_contact = Contact(
            id_document_type=DocumentTypeEnum.PAROISSE.value,
            id_document=paroisse.id,
            **body.model_dump(mode="json", exclude_unset=True)
        )
        session.add(new_contact)
        await session.commit()
        await session.refresh(new_contact)
        projected_response = apply_projection(new_contact, ContactProjFlat, ContactProjShallow, proj)
        return send200(projected_response)

    # Update fields (exclude document identifiers)
    update_data = body.model_dump(
        mode="json", exclude_unset=True, exclude={"id_document_type", "id_document"}
    )
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
    projected_response = apply_projection(contact, ContactProjFlat, ContactProjShallow, proj)
    return send200(projected_response)


@paroisse_router.delete("/{id}/contact", tags=["Paroisse - Contact"])
async def delete_paroisse_contact(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
) -> ContactProjFlat:
    """
    Supprimer le contact associé à un paroisse (hard delete)

    ARGS:
        id (int): L'Id du paroisse
    """

    # Query contact by document type and paroisse id
    contact_stmt = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.PAROISSE.value)
        & (Contact.id_document == paroisse.id)
        & (Contact.est_supprimee == False)
    )
    contact_result = await session.exec(contact_stmt)
    contact = contact_result.first()

    if not contact:
        return send404(["query", "id"], "Contact non trouvé pour ce paroisse")

    contact_proj = ContactProjFlat.model_validate(contact)
    session.delete(contact)
    await session.commit()

    return send200(contact_proj)


# ========================== FIDELES VIEW ENDPOINTS ==========================
from routers.paroisse.fideles import paroisse_fideles_router

paroisse_router.include_router(paroisse_fideles_router)
