from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import Config
from core.db import get_session
from models.fidele import FideleParoisse
from models.fidele.projection import FideleParoisseProjShallowWithoutParoisseData
from models.paroisse import Paroisse
from routers.dependencies import check_resource_exists
from routers.paroisse.docs import PAROISSE_LIST_FIDELES_DESCRIPTION
from routers.utils.http_utils import send200


paroisse_fideles_router = APIRouter(prefix="/{id}/fidele", tags=["Paroisse - Fideles"])


async def required_paroisse(
    id: Annotated[int, Path(..., description="Paroisse's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Paroisse:
    return await check_resource_exists(Paroisse, session, filters={"id": id})


@paroisse_fideles_router.get(
    "",
    summary="Lister les fidèles d'une paroisse",
    description=PAROISSE_LIST_FIDELES_DESCRIPTION,
)
async def list_paroisse_fideles(
    session: Annotated[AsyncSession, Depends(get_session)],
    paroisse: Annotated[Paroisse, Depends(required_paroisse)],
    actif: bool | None = Query(
        True,
        description="Filtrer sur l'appartenance active actuelle (None = tous)",
    ),
    offset: int = 0,
    limit: int = Query(
        Config.PREVIEW_LIST_ITEM_NUMBER.value, ge=1, le=Config.MAX_ITEMS_PER_PAGE.value
    ),
) -> List[FideleParoisseProjShallowWithoutParoisseData]:
    """Lister les fidèles appartenant à une paroisse (via fidele_paroisse)."""

    statement = select(FideleParoisse).where(
        (FideleParoisse.id_paroisse == paroisse.id)
        & (FideleParoisse.est_supprimee == False)
    )
    if actif is not None:
        statement = statement.where(FideleParoisse.est_actif == actif)

    statement = (
        statement
        .options(selectinload(FideleParoisse.fidele))
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(statement)
    items = result.all()

    return send200([
        FideleParoisseProjShallowWithoutParoisseData.model_validate(i) for i in items
    ])
