from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import NiveauEtudes
from models.constants.projections import NiveauEtudesProjFlat
from models.constants.utils import NiveauEtudesBase, NiveauEtudesUpdate
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

niveau_etudes_router = APIRouter(prefix="/niveau_etudes", tags=["Constants - Niveau Etudes"])


async def required_niveau_etudes(
    id: Annotated[int, Path(..., description="NiveauEtudes's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NiveauEtudes:
    return await check_resource_exists(NiveauEtudes, session, filters={"id": id})


@niveau_etudes_router.get("")
async def get_niveaux_etudes(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[NiveauEtudesProjFlat]:
    statement = select(NiveauEtudes).where(NiveauEtudes.est_supprimee == False)
    result = await session.exec(statement)
    niveaux = result.all()
    return send200([NiveauEtudesProjFlat.model_validate(n) for n in niveaux])


@niveau_etudes_router.post("")
async def create_niveau_etudes(
    body: NiveauEtudesBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NiveauEtudesProjFlat:
    niveau = NiveauEtudes.model_validate(body, from_attributes=True)
    session.add(niveau)
    await session.commit()
    await session.refresh(niveau)

    return send200(NiveauEtudesProjFlat.model_validate(niveau))


@niveau_etudes_router.put("/{id}")
async def update_niveau_etudes(
    body: NiveauEtudesUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    niveau: Annotated[NiveauEtudes, Depends(required_niveau_etudes)],
) -> NiveauEtudesProjFlat:
    update_data = body.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(niveau, field, value)

    niveau.date_modification = datetime.now(timezone.utc)

    session.add(niveau)
    await session.commit()

    return send200(NiveauEtudesProjFlat.model_validate(niveau))
