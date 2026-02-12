from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from core.config import Config
from core.db import get_session
from models.direction.fonction import DirectionFonction
from models.direction.fonction.projection import DirectionFonctionProjShallowWithoutFideleData
from models.fidele import Fidele
from routers.fidele.utils import required_fidele
from routers.utils.http_utils import send200


fidele_fonctions_router = APIRouter(prefix="/{id}/fonction", tags=["Fidele - Fonctions"])


@fidele_fonctions_router.get("")
async def list_fidele_fonctions(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    offset: int = 0,
    limit: int = Query(
        Config.PREVIEW_LIST_ITEM_NUMBER.value, ge=1, le=Config.MAX_ITEMS_PER_PAGE.value
    ),
) -> List[DirectionFonctionProjShallowWithoutFideleData]:
    """Lister les mandats (fonctions) d'un fidèle, toutes directions confondues."""

    statement = (
        select(DirectionFonction)
        .where(
            (DirectionFonction.id_fidele == fidele.id)
            & (DirectionFonction.est_supprimee == False)
        )
        .options(
            selectinload(DirectionFonction.direction),
            selectinload(DirectionFonction.fonction),
        )
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(statement)
    items = result.all()

    return send200([
        DirectionFonctionProjShallowWithoutFideleData.model_validate(i) for i in items
    ])
