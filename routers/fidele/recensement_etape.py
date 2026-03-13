from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.constants import RecensementEtape
from models.constants.types import DocumentStatutEnum, RecensementEtapeEnum
from models.fidele import Fidele, FideleRecensementEtape
from models.fidele.projection import FideleRecensementEtapeProjShallow
from routers.fidele.utils import required_fidele
from routers.utils.http_utils import send200

fidele_recensement_etape_router = APIRouter(
    prefix="/{id}/recensement_etape",
    tags=["Fidele - Recensement Etapes"],
)


# ============================================================================
# DEPENDENCIES
# ============================================================================

async def _get_fidele_recensement_etape_with_relations(
    entry: FideleRecensementEtape,
    session: AsyncSession,
) -> FideleRecensementEtape:
    """Re-fetch a FideleRecensementEtape with eager-loaded relations."""
    statement = (
        select(FideleRecensementEtape)
        .where(FideleRecensementEtape.id == entry.id)
        .options(
            selectinload(FideleRecensementEtape.recensement_etape),
            selectinload(FideleRecensementEtape.document_statut),
        )
    )
    result = await session.exec(statement)
    return result.first()


# ============================================================================
# INTERNAL HELPERS  (callable from other endpoints, not exposed as routes)
# ============================================================================

async def upsert_fidele_recensement_etape(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_recensement_etape: int,
    id_document_statut: int,
) -> FideleRecensementEtape:
    """
    Create or update a fidele recensement etape entry.

    - If no entry exists for (id_fidele, id_recensement_etape), one is created.
    - If an entry already exists (even if soft-deleted), it is updated:
        * id_document_statut is set to the new value.
        * est_supprimee is reset to False and date_suppression cleared.
        * date_modification is refreshed.

    Returns the updated/created entry with relations loaded.
    """
    existing_stmt = select(FideleRecensementEtape).where(
        (FideleRecensementEtape.id_fidele == id_fidele)
        & (FideleRecensementEtape.id_recensement_etape == id_recensement_etape)
    )
    result = await session.exec(existing_stmt)
    entry = result.first()

    now = datetime.now(timezone.utc)

    if entry is not None:
        entry.id_document_statut = id_document_statut
        entry.est_supprimee = False
        entry.date_suppression = None
        entry.date_modification = now
    else:
        entry = FideleRecensementEtape(
            id_fidele=id_fidele,
            id_recensement_etape=id_recensement_etape,
            id_document_statut=id_document_statut,
        )

    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return await _get_fidele_recensement_etape_with_relations(entry, session)


async def _upsert_fidele_recensement_etape_without_commit(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_recensement_etape: int,
    id_document_statut: int,
) -> FideleRecensementEtape:
    """Create/update a fidele recensement step without committing the transaction."""
    existing_stmt = select(FideleRecensementEtape).where(
        (FideleRecensementEtape.id_fidele == id_fidele)
        & (FideleRecensementEtape.id_recensement_etape == id_recensement_etape)
    )
    result = await session.exec(existing_stmt)
    entry = result.first()

    now = datetime.now(timezone.utc)

    if entry is not None:
        entry.id_document_statut = id_document_statut
        entry.est_supprimee = False
        entry.date_suppression = None
        entry.date_modification = now
    else:
        entry = FideleRecensementEtape(
            id_fidele=id_fidele,
            id_recensement_etape=id_recensement_etape,
            id_document_statut=id_document_statut,
        )

    session.add(entry)
    await session.flush()
    return entry


async def get_fidele_recensement_completion_details(
    session: AsyncSession,
    *,
    id_fidele: int,
) -> dict[str, int | bool]:
    """Return completion details for a fidele recensement workflow."""
    total_stmt = (
        select(func.count(RecensementEtape.id))
        .where(RecensementEtape.est_supprimee == False)
    )
    total_result = await session.exec(total_stmt)
    total_steps = int(total_result.one() or 0)

    completed_stmt = (
        select(func.count(FideleRecensementEtape.id))
        .where(
            (FideleRecensementEtape.id_fidele == id_fidele)
            & (FideleRecensementEtape.est_supprimee == False)
            & (FideleRecensementEtape.id_document_statut == DocumentStatutEnum.COMPLETE.value)
        )
    )
    completed_result = await session.exec(completed_stmt)
    completed_steps = int(completed_result.one() or 0)

    completion_percentage = 0
    if total_steps > 0:
        completion_percentage = round((completed_steps / total_steps) * 100)

    is_completed = total_steps > 0 and completed_steps >= total_steps
    return {
        "is_completed": is_completed,
        "completed_steps": completed_steps,
        "total_steps": total_steps,
        "completion_percentage": completion_percentage,
    }


async def refresh_fidele_rencensement_statut(
    session: AsyncSession,
    *,
    id_fidele: int,
) -> dict[str, int | bool]:
    """Recompute and persist fidele.rencensement_statut from recensement progress."""
    status_details = await get_fidele_recensement_completion_details(
        session,
        id_fidele=id_fidele,
    )

    fidele_stmt = select(Fidele).where(Fidele.id == id_fidele)
    fidele_result = await session.exec(fidele_stmt)
    fidele = fidele_result.first()

    if fidele is None:
        return status_details

    fidele.rencensement_statut = int(status_details["completion_percentage"])
    fidele.date_modification = datetime.now(timezone.utc)
    session.add(fidele)
    await session.flush()

    return status_details


async def mark_fidele_recensement_etape_completed(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_recensement_etape: RecensementEtapeEnum | int,
) -> dict[str, int | bool]:
    """Mark one recensement step as completed and refresh global fidele status."""
    etape_id = int(id_recensement_etape)

    await _upsert_fidele_recensement_etape_without_commit(
        session,
        id_fidele=id_fidele,
        id_recensement_etape=etape_id,
        id_document_statut=DocumentStatutEnum.COMPLETE.value,
    )

    status_details = await refresh_fidele_rencensement_statut(
        session,
        id_fidele=id_fidele,
    )

    await session.commit()
    return status_details


async def delete_fidele_recensement_etape(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_recensement_etape: int,
) -> FideleRecensementEtape | None:
    """
    Soft-delete the entry for (id_fidele, id_recensement_etape).

    Returns the soft-deleted entry, or None if it did not exist.
    """
    existing_stmt = select(FideleRecensementEtape).where(
        (FideleRecensementEtape.id_fidele == id_fidele)
        & (FideleRecensementEtape.id_recensement_etape == id_recensement_etape)
        & (FideleRecensementEtape.est_supprimee == False)
    )
    result = await session.exec(existing_stmt)
    entry = result.first()

    if entry is None:
        return None

    entry.est_supprimee = True
    entry.date_suppression = datetime.now(timezone.utc)
    entry.date_modification = datetime.now(timezone.utc)

    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


# ============================================================================
# ENDPOINTS
# ============================================================================

@fidele_recensement_etape_router.get("")
async def list_fidele_recensement_etapes(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> List[FideleRecensementEtapeProjShallow]:
    """
    Liste des étapes du recensement complétées (ou en cours) pour un fidèle.
    Note: 
        - Le recensement completé est carracterisé par la presence de l'id du recenseur du l'entité fidele.
        - Quand le candidate a tous ses étapes comme completé, ça veut dire qu'il en attende de la validation de la par d'un fidele abilité.
        - En générale seule les étapes completé seron presentes ici. Car la ligne fidele-recencement-etape est crée seulement lorsque le fidel complete l'étape corespondant.
    
    Returns:
        Liste des entrées triées par id_recensement_etape (ordre naturel des étapes).
    """
    statement = (
        select(FideleRecensementEtape)
        .where(
            (FideleRecensementEtape.id_fidele == fidele.id)
            & (FideleRecensementEtape.est_supprimee == False)
        )
        .options(
            selectinload(FideleRecensementEtape.recensement_etape),
            selectinload(FideleRecensementEtape.document_statut),
        )
        .order_by(FideleRecensementEtape.id_recensement_etape)
    )
    result = await session.exec(statement)
    items = result.all()
    return send200([FideleRecensementEtapeProjShallow.model_validate(i) for i in items])
