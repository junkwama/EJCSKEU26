from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from models.adresse import Adresse, Nation
from models.fidele import (
    Fidele,
    FideleStructure,
    FideleParoisse,
    FideleBapteme,
    FideleOrigine,
    FideleOccupation,
)
from fastapi import Depends, Path
from routers.dependencies import check_resource_exists
from core.db import get_session
from utils.constants import ProjDepth


async def required_fidele(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Fidele:
    return await check_resource_exists(Fidele, session, filters={"id": id})


async def get_fidele_complete_data_by_id(
    id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
) -> Fidele:
    statement = select(Fidele).where(Fidele.id == id)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Fidele.grade),
            selectinload(Fidele.fidele_type),
            selectinload(Fidele.fidele_recenseur),
            selectinload(Fidele.nation_nationalite),
            selectinload(Fidele.etat_civile),
            selectinload(Fidele.document_statut),
            selectinload(Fidele.contact),
            selectinload(Fidele.adresse).selectinload(Adresse.nation).selectinload(Nation.continent),
            selectinload(Fidele.photo),
            selectinload(Fidele.structures).selectinload(FideleStructure.structure),
            selectinload(Fidele.paroisses).selectinload(FideleParoisse.paroisse),
            selectinload(Fidele.bapteme).selectinload(FideleBapteme.paroisse),
            selectinload(Fidele.famille),
            selectinload(Fidele.origine).selectinload(FideleOrigine.nation),
            selectinload(Fidele.occupation).selectinload(FideleOccupation.niveau_etude),
            selectinload(Fidele.occupation).selectinload(FideleOccupation.profession),
        )

    result = await session.exec(statement)
    return result.first()
