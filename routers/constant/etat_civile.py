from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import EtatCivile
from models.constants.projections import EtatCivileProjFlat
from models.constants.utils import EtatCivileBase, EtatCivileUpdate
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

etat_civile_router = APIRouter(prefix="/etat_civile", tags=["Constants - Etat Civile"])


async def required_etat_civile(
    id: Annotated[int, Path(..., description="EtatCivile's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EtatCivile:
    return await check_resource_exists(EtatCivile, session, filters={"id": id})


@etat_civile_router.get("")
async def get_etats_civiles(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[EtatCivileProjFlat]:
    statement = select(EtatCivile).where(EtatCivile.est_supprimee == False)
    result = await session.exec(statement)
    etats = result.all()
    return send200([EtatCivileProjFlat.model_validate(e) for e in etats])


@etat_civile_router.post("")
async def create_etat_civile(
    body: EtatCivileBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EtatCivileProjFlat:
    etat = EtatCivile.model_validate(body, from_attributes=True)
    session.add(etat)
    await session.commit()
    await session.refresh(etat)

    return send200(EtatCivileProjFlat.model_validate(etat))


@etat_civile_router.put("/{id}")
async def update_etat_civile(
    body: EtatCivileUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    etat: Annotated[EtatCivile, Depends(required_etat_civile)],
) -> EtatCivileProjFlat:
    update_data = body.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(etat, field, value)

    etat.date_modification = datetime.now(timezone.utc)

    session.add(etat)
    await session.commit()

    return send200(EtatCivileProjFlat.model_validate(etat))
