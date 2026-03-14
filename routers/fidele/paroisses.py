from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.constants.types import RecensementEtapeEnum
from models.fidele import Fidele, FideleParoisse
from models.fidele.projection import (
    FideleParoisseProjFlat,
    FideleParoisseProjShallowWithoutFideleData,
)
from models.fidele.utils import FideleParoisseCreate, FideleParoisseUpdate
from models.paroisse import Paroisse
from routers.utils import check_resource_exists
from routers.fidele.recensement_etape import mark_fidele_recensement_etape_completed
from routers.fidele.utils import required_fidele
from routers.utils.http_utils import send200, send400


fidele_paroisses_router = APIRouter(prefix="/{id}/paroisse", tags=["Fidele - Paroisses"])


async def _count_active_fidele_paroisses(session: AsyncSession, *, id_fidele: int) -> int:
    statement = select(FideleParoisse).where(
        (FideleParoisse.id_fidele == id_fidele)
        & (FideleParoisse.est_supprimee == False)
    )
    result = await session.exec(statement)
    return len(result.all())


async def _set_unique_principale_paroisse(
    session: AsyncSession,
    *,
    id_fidele: int,
    keep_membership_id: int,
) -> None:
    statement = select(FideleParoisse).where(
        (FideleParoisse.id_fidele == id_fidele)
        & (FideleParoisse.est_supprimee == False)
    )
    result = await session.exec(statement)
    memberships = result.all()

    now = datetime.now(timezone.utc)
    for membership in memberships:
        should_be_principale = membership.id == keep_membership_id
        if membership.est_paroisse_principale != should_be_principale:
            membership.est_paroisse_principale = should_be_principale
            membership.date_modification = now
            session.add(membership)

    await session.commit()


def are_membership_dates_valid(date_adhesion: date | None, date_sortie: date | None) -> bool:
    if date_adhesion and date_sortie and date_sortie < date_adhesion:
        return False
    return True


def compute_est_actif(date_sortie: date | None) -> bool:
    if date_sortie is None:
        return True
    return date_sortie >= date.today()


async def get_fidele_paroisse_complete_data_by_id(
    fidele_paroisse_id: int,
    session: AsyncSession,
) -> FideleParoisse | None:
    statement = (
        select(FideleParoisse)
        .where(FideleParoisse.id == fidele_paroisse_id)
        .options(selectinload(FideleParoisse.paroisse))
    )
    result = await session.exec(statement)
    return result.first()


async def required_fidele_paroisse(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    id_paroisse: Annotated[int, Path(..., description="Paroisse's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleParoisse:
    return await check_resource_exists(
        FideleParoisse,
        session,
        filters={"id_fidele": id, "id_paroisse": id_paroisse},
    )


@fidele_paroisses_router.post("")
async def add_fidele_paroisse(
    body: FideleParoisseCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleParoisseProjShallowWithoutFideleData:
    """Ajouter une paroisse à un fidèle (historique d'appartenance)."""

    await check_resource_exists(Paroisse, session, filters={"id": body.id_paroisse})

    if not are_membership_dates_valid(body.date_adhesion, body.date_sortie):
        return send400(["body"], "Dates d'adhésion/sortie invalides")

    existing_stmt = select(FideleParoisse).where(
        (FideleParoisse.id_fidele == fidele.id)
        & (FideleParoisse.id_paroisse == body.id_paroisse)
    )
    existing_result = await session.exec(existing_stmt)
    existing = existing_result.first()

    if existing and existing.est_supprimee == False:
        return send400(["body", "id_paroisse"], "Ce fidèle appartient déjà à cette paroisse")

    if existing and existing.est_supprimee == True:
        active_count = await _count_active_fidele_paroisses(session, id_fidele=fidele.id)
        should_be_principale = bool(body.est_paroisse_principale)
        if active_count == 0:
            should_be_principale = True

        existing.est_supprimee = False
        existing.date_suppression = None
        existing.date_adhesion = body.date_adhesion
        existing.date_sortie = body.date_sortie
        existing.est_actif = compute_est_actif(body.date_sortie)
        existing.est_paroisse_principale = should_be_principale
        existing.date_modification = datetime.now(timezone.utc)

        session.add(existing)
        await session.commit()
        await session.refresh(existing)

        if should_be_principale:
            await _set_unique_principale_paroisse(
                session,
                id_fidele=fidele.id,
                keep_membership_id=existing.id,
            )

        await mark_fidele_recensement_etape_completed(
            session,
            id_fidele=fidele.id,
            id_recensement_etape=RecensementEtapeEnum.PAROISSES,
        )

        existing = await get_fidele_paroisse_complete_data_by_id(existing.id, session)
        return send200(FideleParoisseProjShallowWithoutFideleData.model_validate(existing))

    active_count = await _count_active_fidele_paroisses(session, id_fidele=fidele.id)
    should_be_principale = bool(body.est_paroisse_principale)
    if active_count == 0:
        should_be_principale = True

    fidele_paroisse = FideleParoisse(
        id_fidele=fidele.id,
        id_paroisse=body.id_paroisse,
        date_adhesion=body.date_adhesion,
        date_sortie=body.date_sortie,
        est_actif=compute_est_actif(body.date_sortie),
        est_paroisse_principale=should_be_principale,
    )

    session.add(fidele_paroisse)
    await session.commit()
    await session.refresh(fidele_paroisse)

    if should_be_principale:
        await _set_unique_principale_paroisse(
            session,
            id_fidele=fidele.id,
            keep_membership_id=fidele_paroisse.id,
        )

    await mark_fidele_recensement_etape_completed(
        session,
        id_fidele=fidele.id,
        id_recensement_etape=RecensementEtapeEnum.PAROISSES,
    )

    fidele_paroisse = await get_fidele_paroisse_complete_data_by_id(fidele_paroisse.id, session)
    return send200(FideleParoisseProjShallowWithoutFideleData.model_validate(fidele_paroisse))


@fidele_paroisses_router.get("")
async def list_fidele_paroisses(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> List[FideleParoisseProjShallowWithoutFideleData]:
    """Lister les paroisses (historique d'appartenance) d'un fidèle."""

    statement = (
        select(FideleParoisse)
        .where(
            (FideleParoisse.id_fidele == fidele.id)
            & (FideleParoisse.est_supprimee == False)
        )
        .options(selectinload(FideleParoisse.paroisse))
    )
    result = await session.exec(statement)
    items = result.all()

    return send200([FideleParoisseProjShallowWithoutFideleData.model_validate(i) for i in items])


@fidele_paroisses_router.put("/{id_paroisse}")
async def update_fidele_paroisse(
    body: FideleParoisseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele_paroisse: Annotated[FideleParoisse, Depends(required_fidele_paroisse)],
) -> FideleParoisseProjFlat:
    """Mettre à jour les dates d'appartenance d'un fidèle dans une paroisse."""

    update_data = body.model_dump(mode="json", exclude_unset=True)

    effective_date_adhesion = update_data.get("date_adhesion", fidele_paroisse.date_adhesion)
    effective_date_sortie = update_data.get("date_sortie", fidele_paroisse.date_sortie)
    if not are_membership_dates_valid(effective_date_adhesion, effective_date_sortie):
        return send400(["body"], "Dates d'adhésion/sortie invalides")

    requested_principale = update_data.get("est_paroisse_principale")

    for field, value in update_data.items():
        setattr(fidele_paroisse, field, value)

    fidele_paroisse.est_actif = compute_est_actif(effective_date_sortie)

    fidele_paroisse.date_modification = datetime.now(timezone.utc)

    session.add(fidele_paroisse)
    await session.commit()
    await session.refresh(fidele_paroisse)

    if requested_principale is True:
        await _set_unique_principale_paroisse(
            session,
            id_fidele=fidele_paroisse.id_fidele,
            keep_membership_id=fidele_paroisse.id,
        )

    return send200(FideleParoisseProjFlat.model_validate(fidele_paroisse))


@fidele_paroisses_router.delete("/{id_paroisse}")
async def remove_fidele_paroisse(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele_paroisse: Annotated[FideleParoisse, Depends(required_fidele_paroisse)],
) -> FideleParoisseProjFlat:
    """Supprimer (soft delete) l'appartenance d'un fidèle à une paroisse."""

    fidele_paroisse.est_supprimee = True
    fidele_paroisse.est_actif = False
    fidele_paroisse.est_paroisse_principale = False
    fidele_paroisse.date_suppression = datetime.now(timezone.utc)
    fidele_paroisse.date_modification = datetime.now(timezone.utc)

    session.add(fidele_paroisse)
    await session.commit()

    return send200(FideleParoisseProjFlat.model_validate(fidele_paroisse))
