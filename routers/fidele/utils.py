from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from models.fidele import Fidele
from fastapi import Depends, Path
from routers.dependencies import check_resource_exists
from core.db import get_session


async def required_fidele(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Fidele:
    return await check_resource_exists(Fidele, session, filters={"id": id})
