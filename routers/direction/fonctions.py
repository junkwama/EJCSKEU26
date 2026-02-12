from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import Config
from core.db import get_session
from models.constants import Fonction
from models.direction import Direction
from models.direction.fonction import DirectionFonction
from models.direction.fonction.projection import (
    DirectionFonctionProjFlat,
    DirectionFonctionProjShallowWithoutDirectionData,
)
from models.direction.fonction.utils import DirectionFonctionCreate, DirectionFonctionUpdate
from models.fidele import Fidele
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200, send400, send404
from sqlalchemy.orm import selectinload


direction_fonctions_router = APIRouter(prefix="/{id}/fonctions", tags=["Direction - Fonctions"])


def are_mandate_dates_valid(date_debut: date, date_fin: date | None) -> bool:
    if date_fin is not None and date_fin < date_debut:
        return False
    return True


def compute_est_actif(date_fin: date | None, est_suspendu: bool) -> bool:
    if est_suspendu:
        return False
    if date_fin is None:
        return True
    return date_fin >= date.today()


async def required_direction_fonction(
    id: Annotated[int, Path(..., description="Direction ID")],
    id_direction_fonction: Annotated[int, Path(..., description="DirectionFonction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DirectionFonction:
    return await check_resource_exists(
        DirectionFonction,
        session,
        filters={"id": id_direction_fonction, "id_direction": id},
    )


async def get_direction_fonction_any_by_id(
    direction_id: int,
    direction_fonction_id: int,
    session: AsyncSession,
) -> DirectionFonction | None:
    statement = select(DirectionFonction).where(
        (DirectionFonction.id == direction_fonction_id)
        & (DirectionFonction.id_direction == direction_id)
    )
    result = await session.exec(statement)
    return result.first()


async def get_direction_fonction_complete_data_by_id(
    direction_id: int,
    direction_fonction_id: int,
    session: AsyncSession,
) -> DirectionFonction | None:
    statement = (
        select(DirectionFonction)
        .where(
            (DirectionFonction.id == direction_fonction_id)
            & (DirectionFonction.id_direction == direction_id)
        )
        .options(
            selectinload(DirectionFonction.fidele),
            selectinload(DirectionFonction.fonction),
        )
    )
    result = await session.exec(statement)
    return result.first()


@direction_fonctions_router.post("")
async def create_direction_fonction(
    id: Annotated[int, Path(..., description="Direction ID")],
    body: DirectionFonctionCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DirectionFonctionProjShallowWithoutDirectionData:
    """Assigner un fidèle à une fonction dans une direction."""

    await check_resource_exists(Direction, session, filters={"id": id})
    await check_resource_exists(Fidele, session, filters={"id": body.id_fidele})
    await check_resource_exists(Fonction, session, filters={"id": body.id_fonction})

    if not are_mandate_dates_valid(body.date_debut, body.date_fin):
        return send400(["body"], "Dates de mandat invalides")

    est_actif = compute_est_actif(body.date_fin, body.est_suspendu)

    item = DirectionFonction(
        id_direction=id,
        id_fidele=body.id_fidele,
        id_fonction=body.id_fonction,
        date_debut=body.date_debut,
        date_fin=body.date_fin,
        est_suspendu=body.est_suspendu,
        est_actif=est_actif,
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    item = await get_direction_fonction_complete_data_by_id(id, item.id, session)
    return send200(DirectionFonctionProjShallowWithoutDirectionData.model_validate(item))


@direction_fonctions_router.get("")
async def list_direction_fonctions(
    id: Annotated[int, Path(..., description="Direction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(
        Config.PREVIEW_LIST_ITEM_NUMBER.value, ge=1, le=Config.MAX_ITEMS_PER_PAGE.value
    ),
) -> List[DirectionFonctionProjFlat]:
    """Lister les mandats (fonctions) d'une direction."""

    await check_resource_exists(Direction, session, filters={"id": id})

    statement = (
        select(DirectionFonction)
        .where((DirectionFonction.id_direction == id) & (DirectionFonction.est_supprimee == False))
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(statement)
    items = result.all()

    return send200([DirectionFonctionProjFlat.model_validate(i) for i in items])


@direction_fonctions_router.get("/{id_direction_fonction}")
async def get_direction_fonction(
    id: Annotated[int, Path(..., description="Direction ID")],
    id_direction_fonction: Annotated[int, Path(..., description="DirectionFonction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[DirectionFonction, Depends(required_direction_fonction)],
) -> DirectionFonctionProjShallowWithoutDirectionData:
    item = await get_direction_fonction_complete_data_by_id(id, id_direction_fonction, session)
    return send200(DirectionFonctionProjShallowWithoutDirectionData.model_validate(item))


@direction_fonctions_router.put("/{id_direction_fonction}")
async def update_direction_fonction(
    body: DirectionFonctionUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    direction_fonction: Annotated[DirectionFonction, Depends(required_direction_fonction)],
) -> DirectionFonctionProjShallowWithoutDirectionData:
    """Mettre à jour dates/statut d'un mandat, en gardant la cohérence date_fin/est_actif."""

    update_data = body.model_dump(mode="json", exclude_unset=True)

    effective_date_debut = update_data.get("date_debut", direction_fonction.date_debut)
    effective_date_fin = update_data.get("date_fin", direction_fonction.date_fin)

    if not are_mandate_dates_valid(effective_date_debut, effective_date_fin):
        return send400(["body"], "Dates de mandat invalides")

    effective_est_suspendu = update_data.get("est_suspendu", direction_fonction.est_suspendu)
    effective_est_actif = compute_est_actif(effective_date_fin, effective_est_suspendu)

    for field, value in update_data.items():
        setattr(direction_fonction, field, value)

    direction_fonction.est_actif = effective_est_actif
    direction_fonction.date_modification = datetime.now(timezone.utc)

    session.add(direction_fonction)
    await session.commit()
    await session.refresh(direction_fonction)

    item = await get_direction_fonction_complete_data_by_id(
        direction_fonction.id_direction, direction_fonction.id, session
    )
    return send200(DirectionFonctionProjShallowWithoutDirectionData.model_validate(item))


@direction_fonctions_router.put("/{id_direction_fonction}/restore")
async def restore_direction_fonction(
    id: Annotated[int, Path(..., description="Direction ID")],
    id_direction_fonction: Annotated[int, Path(..., description="DirectionFonction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DirectionFonctionProjShallowWithoutDirectionData:
    item = await get_direction_fonction_any_by_id(id, id_direction_fonction, session)
    if not item:
        return send404(["path", "id_direction_fonction"], "Mandat non trouvé")

    if item.est_supprimee:
        item.est_supprimee = False
        item.date_suppression = None
        item.est_actif = compute_est_actif(item.date_fin, item.est_suspendu)
        item.date_modification = datetime.now(timezone.utc)

        session.add(item)
        await session.commit()
        await session.refresh(item)

    item = await get_direction_fonction_complete_data_by_id(id, item.id, session)
    return send200(DirectionFonctionProjShallowWithoutDirectionData.model_validate(item))


@direction_fonctions_router.delete("/{id_direction_fonction}")
async def delete_direction_fonction(
    session: Annotated[AsyncSession, Depends(get_session)],
    direction_fonction: Annotated[DirectionFonction, Depends(required_direction_fonction)],
) -> DirectionFonctionProjFlat:
    """Soft delete un mandat."""

    direction_fonction.est_supprimee = True
    direction_fonction.date_suppression = datetime.now(timezone.utc)
    direction_fonction.date_modification = datetime.now(timezone.utc)
    direction_fonction.est_actif = False

    session.add(direction_fonction)
    await session.commit()

    return send200(DirectionFonctionProjFlat.model_validate(direction_fonction))
