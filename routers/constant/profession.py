from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import Profession
from models.constants.projections import ProfessionProjFlat
from models.constants.utils import ProfessionBase, ProfessionUpdate
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

profession_router = APIRouter(prefix="/profession", tags=["Constants - Professions"])


async def required_profession(
    id: Annotated[int, Path(..., description="Profession's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Profession:
    return await check_resource_exists(Profession, session, filters={"id": id})


@profession_router.get("")
async def get_professions(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[ProfessionProjFlat]:
    statement = select(Profession).where(Profession.est_supprimee == False)
    result = await session.exec(statement)
    professions = result.all()
    return send200([ProfessionProjFlat.model_validate(p) for p in professions])


@profession_router.post("")
async def create_profession(
    body: ProfessionBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProfessionProjFlat:
    profession = Profession.model_validate(body, from_attributes=True)
    session.add(profession)
    await session.commit()
    await session.refresh(profession)

    return send200(ProfessionProjFlat.model_validate(profession))


@profession_router.put("/{id}")
async def update_profession(
    body: ProfessionUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    profession: Annotated[Profession, Depends(required_profession)],
) -> ProfessionProjFlat:
    update_data = body.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(profession, field, value)

    profession.date_modification = datetime.now(timezone.utc)

    session.add(profession)
    await session.commit()

    return send200(ProfessionProjFlat.model_validate(profession))
