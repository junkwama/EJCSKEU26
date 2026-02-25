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
from models.fidele import (
    Fidele,
    FideleFamille,
    FideleOrigine,
    FideleOccupation,
)
from models.fidele.utils import FideleBase, FideleUpdate
from models.fidele.projection import FideleProjFlat, FideleProjFlatWithPhoto, FideleProjShallow
from models.adresse import Adresse, Nation
from models.adresse.utils import AdresseUpdate
from models.adresse.projection import AdresseProjFlat, AdresseProjShallow
from models.contact import Contact
from models.contact.utils import ContactUpdate
from models.contact.projection import ContactProjFlat, ContactProjShallow
from core.db import get_session
from routers.fidele.utils import (
    required_fidele,
    get_fidele_complete_data_by_id,
    parse_fidele_include,
)
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200, send404
from routers.utils import apply_projection
from utils.constants import ProjDepth
from models.constants import DocumentType, FideleType, Grade, EtatCivile, DocumentStatut

fidele_router = APIRouter()


async def get_fidele_any_by_id(fidele_id: int, session: AsyncSession) -> Fidele | None:
    statement = select(Fidele).where(Fidele.id == fidele_id)
    result = await session.exec(statement)
    return result.first()


async def get_fidele_adresse_complete_data_by_id(
    fidele_id: int, session: AsyncSession, proj: ProjDepth = ProjDepth.SHALLOW
) -> Adresse:
    statement = (
        select(Adresse)
        .where(
            (Adresse.id_document_type == DocumentTypeEnum.FIDELE.value)
            & (Adresse.id_document == fidele_id)
            & (Adresse.est_supprimee == False)
        )
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Adresse.nation).selectinload(Nation.continent)
        )

    result = await session.exec(statement)
    return result.first()


@fidele_router.post("", tags=["Fidele"])
async def create_fidele(
    body: FideleBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleProjShallow | FideleProjFlat:
    """
    Créer un nouveau fidele

    ARGS:
        body (FideleBase): Les données du fidele à créer
    """
    await check_resource_exists(Grade, session, filters={"id": int(body.id_grade)})
    await check_resource_exists(
        FideleType, session, filters={"id": int(body.id_fidele_type)}
    )
    if body.id_fidele_recenseur is not None:
        await check_resource_exists(Fidele, session, filters={"id": body.id_fidele_recenseur})
    if body.id_nation_nationalite is not None:
        await check_resource_exists(Nation, session, filters={"id": body.id_nation_nationalite})
    if body.id_etat_civile is not None:
        await check_resource_exists(EtatCivile, session, filters={"id": body.id_etat_civile})
    await check_resource_exists(DocumentStatut, session, filters={"id": int(body.id_document_statut)})

    # Create new fidele instance
    fidele = Fidele(**body.model_dump(mode="json"))
    fidele.code_matriculation = None

    # Add to session and commit
    session.add(fidele)
    await session.commit()
    await session.refresh(fidele)

    # re-fetch to get related data for shallow projection
    if proj == ProjDepth.SHALLOW:
        fidele = await get_fidele_complete_data_by_id(fidele.id, session, proj)

    # Return the created fidele
    projected_response = apply_projection(fidele, FideleProjFlat, FideleProjShallow, proj)
    return send200(projected_response)


@fidele_router.get("", tags=["Fidele"])
async def get_fideles(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(Config.PREVIEW_LIST_ITEM_NUMBER, ge=1, le=Config.MAX_ITEMS_PER_PAGE),
    include: Annotated[
        str | None,
        Query(description="Relations à inclure en flat (ex: photo)")
    ] = None,
) -> List[FideleProjFlat | FideleProjFlatWithPhoto]:
    """
    Recuperer la liste des fideles avec pagination
    """
    # Fetching main data
    include_fields = parse_fidele_include(include)
    should_include_photo = "photo" in include_fields

    statement = (
        select(Fidele)
        .where(Fidele.est_supprimee == False)
        .offset(offset)
        .limit(limit)
    )
    if should_include_photo:
        statement = statement.options(selectinload(Fidele.photo))

    result = await session.exec(statement)
    fidele_list = result.all()

    # Returning the list
    flat_projection = FideleProjFlatWithPhoto if should_include_photo else FideleProjFlat
    return send200([flat_projection.model_validate(fidele) for fidele in fidele_list])


@fidele_router.get("/{id}", tags=["Fidele"])
async def get_fidele(
    id: Annotated[int, Path(..., description="Fidele's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[AsyncSession, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
    include: Annotated[
        str | None,
        Query(description="Relations à inclure en flat (ex: photo)")
    ] = None,
) -> FideleProjShallow | FideleProjFlat | FideleProjFlatWithPhoto:
    """
    Recuperer un fidele par son Id avec ses relations

    ARGS:
        id (int): L'Id du fidele à récupérer
    """
    include_fields = parse_fidele_include(include)
    should_include_photo = proj == ProjDepth.FLAT and "photo" in include_fields

    # Fetching related data for the shallow projection
    if proj == ProjDepth.SHALLOW or should_include_photo:
        fidele = await get_fidele_complete_data_by_id(id, session, proj, include_fields)

    # Return the fidele as projection
    flat_projection = FideleProjFlatWithPhoto if should_include_photo else FideleProjFlat
    projected_response = apply_projection(fidele, flat_projection, FideleProjShallow, proj)
    return send200(projected_response)


@fidele_router.put("/{id}", tags=["Fidele"])
async def update_fidele(
    body: FideleUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleProjShallow | FideleProjFlat:
    """
    Modifier un fidele existant

    ARGS:
        id (int): L'Id du fidele à modifier
        body (FideleUpdate): Les données mises à jour du fidele
    """

    update_data = body.model_dump(mode="json", exclude_unset=True)

    if "id_grade" in update_data and update_data["id_grade"] is not None:
        await check_resource_exists(Grade, session, filters={"id": int(update_data["id_grade"])})
    if "id_fidele_type" in update_data and update_data["id_fidele_type"] is not None:
        await check_resource_exists(
            FideleType, session, filters={"id": int(update_data["id_fidele_type"]) }
        )
    if "id_fidele_recenseur" in update_data and update_data["id_fidele_recenseur"] is not None:
        await check_resource_exists(Fidele, session, filters={"id": update_data["id_fidele_recenseur"]})
    if "id_nation_nationalite" in update_data and update_data["id_nation_nationalite"] is not None:
        await check_resource_exists(Nation, session, filters={"id": update_data["id_nation_nationalite"]})
    if "id_etat_civile" in update_data and update_data["id_etat_civile"] is not None:
        await check_resource_exists(EtatCivile, session, filters={"id": update_data["id_etat_civile"]})
    if "id_document_statut" in update_data and update_data["id_document_statut"] is not None:
        await check_resource_exists(DocumentStatut, session, filters={"id": update_data["id_document_statut"]})

    # Update fields (only provided fields)
    for field, value in update_data.items():
        setattr(fidele, field, value)

    # Update modification timestamp
    fidele.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(fidele)
    await session.commit()

    # Re-query with eager loads so relationships are available for projection
    if proj == ProjDepth.SHALLOW:
        fidele = await get_fidele_complete_data_by_id(fidele.id, session, proj)

    # Return the updated fidele with related objects already loaded
    projected_response = apply_projection(fidele, FideleProjFlat, FideleProjShallow, proj)
    return send200(projected_response)


@fidele_router.put("/{id}/restore", tags=["Fidele"])
async def restore_fidele(
    id: Annotated[int, Path(..., description="Fidele's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleProjShallow | FideleProjFlat:
    """
    Restaurer un fidele supprimé (soft delete)

    ARGS:
        id (int): L'Id du fidele à restaurer
    """

    fidele = await get_fidele_any_by_id(id, session)
    if not fidele:
        return send404(["path", "id"], "Fidele non trouvé")

    # If already is deleted, restore
    if fidele.est_supprimee:

        fidele.est_supprimee = False
        fidele.date_suppression = None
        fidele.date_modification = datetime.now(timezone.utc)

        session.add(fidele)
        await session.commit()

    # Re-query with eager loads so relationships are available for projection
    if proj == ProjDepth.SHALLOW:
        fidele = await get_fidele_complete_data_by_id(fidele.id, session, proj)

    projected_response = apply_projection(fidele, FideleProjFlat, FideleProjShallow, proj)
    return send200(projected_response)

@fidele_router.delete("/{id}", tags=["Fidele"])
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

    projected_fidele = FideleProjFlat.model_validate(fidele)
    return send200(projected_fidele)


# ========================== ADRESSE ENDPOINTS ==========================
@fidele_router.get("/{id}/adresse", tags=["Fidele - Adresse"])
async def get_fidele_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Récupérer l'adresse associée à un fidele

    ARGS:
        id (int): L'Id du fidele
    """

    # Query adresse by document type (FIDELE=1) and fidele id
    adresse = await get_fidele_adresse_complete_data_by_id(fidele.id, session, proj)

    if not adresse:
        return send404(["query", "id"], "Adresse non trouvée pour ce fidele")

    projected_response = apply_projection(adresse, AdresseProjFlat, AdresseProjShallow, proj)
    return send200(projected_response)


@fidele_router.put("/{id}/adresse", tags=["Fidele - Adresse"])
async def update_fidele_adresse(
    body: AdresseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Modifier l'adresse associée à un fidele

    ARGS:
        id (int): L'Id du fidele
        body (AdresseUpdate): Les données mises à jour de l'adresse
    """

    # Query adresse by document type (FIDELE=1) and fidele id
    adresse = await get_fidele_adresse_complete_data_by_id(fidele.id, session, proj)

    if not adresse:
        if body.id_nation is not None:
            await check_resource_exists(Nation, session, filters={"id": body.id_nation})
        await check_resource_exists(
            DocumentType, session, filters={"id": DocumentTypeEnum.FIDELE.value}
        )
        # Create new adresse if not found
        new_adresse = Adresse(
            id_document_type=DocumentTypeEnum.FIDELE.value,
            id_document=fidele.id,
            **body.model_dump(mode="json", exclude_unset=True)
        )
        session.add(new_adresse)
        await session.commit()
        await session.refresh(new_adresse)

        if proj == ProjDepth.SHALLOW: # if shallow fetc related data
            new_adresse = await get_fidele_adresse_complete_data_by_id(fidele.id, session, proj)

        projected_response = apply_projection(new_adresse, AdresseProjFlat, AdresseProjShallow, proj)
        return send200(projected_response)

    # Update fields (exclude document identifiers)
    update_data = body.model_dump(
        mode="json", exclude_unset=True, exclude={"id_document_type", "id_document"}
    )
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


@fidele_router.delete("/{id}/adresse", tags=["Fidele - Adresse"])
async def delete_fidele_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> AdresseProjFlat:
    """
    Supprimer l'adresse associée à un fidele (hard delete)

    ARGS:
        id (int): L'Id du fidele
    """

    # Query adresse
    adresse = await get_fidele_adresse_complete_data_by_id(fidele.id, session, ProjDepth.FLAT)

    if not adresse:
        return send404(["query", "id"], "Adresse non trouvée pour ce fidele")

    # Convert to projection BEFORE deletion
    adresse_proj = AdresseProjFlat.model_validate(adresse)

    # Hard delete
    session.delete(adresse)
    await session.commit()

    return send200(adresse_proj)


# ========================== CONTACT ENDPOINTS ==========================

@fidele_router.get("/{id}/contact", tags=["Fidele - Contact"])
async def get_fidele_contact(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ContactProjShallow | ContactProjFlat:
    """
    Récupérer le contact associée à un fidele

    ARGS:
        id (int): L'Id du fidele
    """
    # Query contact by document type (FIDELE=1) and fidele id
    statement = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (Contact.id_document == fidele.id)
        & (Contact.est_supprimee == False)
    )
    contact_result = await session.exec(statement)
    contact = contact_result.first()

    if not contact:
        return send404(["query", "id"], "Contact non trouvé pour ce fidele")

    projected_response = apply_projection(contact, ContactProjFlat, ContactProjShallow, proj)
    return send200(projected_response)


@fidele_router.put("/{id}/contact", tags=["Fidele - Contact"])
async def update_fidele_contact(
    body: ContactUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> ContactProjShallow | ContactProjFlat:
    """
    Modifier le contact associé à un fidele

    ARGS:
        id (int): L'Id du fidele
        body (ContactUpdate): Les données mises à jour du contact
    """

    # Query contact by document type (FIDELE=1) and fidele id
    contact_stmt = select(Contact).where(
        (Contact.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (Contact.id_document == fidele.id)
    )
    contact_result = await session.exec(contact_stmt)
    contact = contact_result.first()

    if not contact:
        await check_resource_exists(
            DocumentType, session, filters={"id": DocumentTypeEnum.FIDELE.value}
        )
        # Create new contact if not found
        new_contact = Contact(
            id_document_type=DocumentTypeEnum.FIDELE.value,
            id_document=fidele.id,
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


@fidele_router.delete("/{id}/contact", tags=["Fidele - Contact"])
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
        (Contact.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (Contact.id_document == fidele.id)
    )
    contact_result = await session.exec(contact_stmt)
    contact = contact_result.first()

    if not contact:
        return send404(["query", "id"], "Contact non trouvé pour ce fidele")

    contact_proj = ContactProjFlat.model_validate(contact)
    session.delete(contact)
    await session.commit()

    return send200(contact_proj)


# ========================== SUB DATA ENDPOINTS ==========================
from routers.fidele.photo import fidele_photo_router
fidele_router.include_router(fidele_photo_router)

from routers.fidele.structures import fidele_structures_router
fidele_router.include_router(fidele_structures_router)

from routers.fidele.paroisses import fidele_paroisses_router
fidele_router.include_router(fidele_paroisses_router)

from routers.fidele.bapteme import fidele_bapteme_router
fidele_router.include_router(fidele_bapteme_router)

from routers.fidele.famille import fidele_famille_router
fidele_router.include_router(fidele_famille_router)

from routers.fidele.origine import fidele_origine_router
fidele_router.include_router(fidele_origine_router)

from routers.fidele.occupation import fidele_occupation_router
fidele_router.include_router(fidele_occupation_router)

from routers.fidele.fonctions import fidele_fonctions_router
fidele_router.include_router(fidele_fonctions_router)

from routers.fidele.statut import fidele_statut_router
fidele_router.include_router(fidele_statut_router)
