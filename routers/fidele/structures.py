from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from core.db import get_session
from models.constants import Structure
from models.fidele import Fidele, FideleStructure
from models.fidele.utils import FideleStructureCreate
from models.fidele.projection import (
    FideleStructureProjFlat,
    FideleStructureProjShallowWithoutFideleData,
)
from routers.dependencies import check_resource_exists
from routers.fidele.docs import FIDELE_ADD_STRUCTURE_DESCRIPTION
from routers.utils.http_utils import send200, send400
from routers.fidele.utils import required_fidele

fidele_structures_router = APIRouter(prefix="/{id}/structure", tags=["Fidele - Structures"])


async def get_fidele_structure_complete_data_by_id(
    fidele_structure_id: int,
    session: AsyncSession,
) -> FideleStructure | None:
    statement = (
        select(FideleStructure)
        .where(FideleStructure.id == fidele_structure_id)
        .options(selectinload(FideleStructure.structure))
    )
    result = await session.exec(statement)
    return result.first()

async def required_fidele_structure(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    id_structure: Annotated[int, Path(..., description="Structure's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleStructure:
    return await check_resource_exists(FideleStructure, session, filters={
        "id_fidele": id, 
        "id_structure": id_structure
    })

@fidele_structures_router.post(
    "",
    summary="Ajouter une structure à un fidèle (adhésion)",
    description=FIDELE_ADD_STRUCTURE_DESCRIPTION,
)
async def add_fidele_structure(
    body: FideleStructureCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleStructureProjShallowWithoutFideleData:
    """Ajouter une structure à un fidèle (crée une adhésion dans fidele_structure)."""

    # Structure id=1 is the "bureau ecclésiatique": no generic membership allowed.
    # Access is managed via direction mandats (/direction/{id}/fonctions) instead.
    if int(body.id_structure) == 1:
        return send400(
            ["body", "id_structure"],
            "Adhésion interdite: la structure 'Bureau ecclésiatique' (id=1) n'a pas de membres génériques. "
            "Utilisez plutôt les mandats/fonctions (direction_fonction).",
        )

    # Ensure structure exists
    await check_resource_exists(Structure, session, filters={"id": body.id_structure})

    # Check existing membership (active or soft-deleted)
    existing_stmt = select(FideleStructure).where(
        (FideleStructure.id_fidele == fidele.id)
        & (FideleStructure.id_structure == body.id_structure)
    )
    existing_result = await session.exec(existing_stmt)
    existing = existing_result.first()

    if existing and existing.est_supprimee == False:
        return send400(["body", "id_structure"], "Ce fidèle appartient déjà à cette structure")

    if existing and existing.est_supprimee == True:
        if int(body.id_structure) == 1:
            return send400(
                ["body", "id_structure"],
                "Restauration interdite: la structure 'Bureau ecclésiatique' (id=1) n'a pas de membres génériques. "
                "Utilisez plutôt les mandats/fonctions (direction_fonction).",
            )

        existing.est_supprimee = False
        existing.date_suppression = None
        existing.date_modification = datetime.now(timezone.utc)

        session.add(existing)
        await session.commit()
        await session.refresh(existing)

        existing = await get_fidele_structure_complete_data_by_id(existing.id, session)

        return send200(FideleStructureProjShallowWithoutFideleData.model_validate(existing))

    fidele_structure = FideleStructure(
        id_fidele=fidele.id,
        id_structure=body.id_structure,
    )

    session.add(fidele_structure)
    await session.commit()
    await session.refresh(fidele_structure)

    fidele_structure = await get_fidele_structure_complete_data_by_id(fidele_structure.id, session)

    return send200(FideleStructureProjShallowWithoutFideleData.model_validate(fidele_structure))


@fidele_structures_router.get("")
async def list_fidele_structures(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> List[FideleStructureProjShallowWithoutFideleData]:
    """Lister les structures (adhésions) d'un fidèle."""

    statement = (
        select(FideleStructure)
        .where(
            (FideleStructure.id_fidele == fidele.id)
            & (FideleStructure.est_supprimee == False)
        )
        .options(selectinload(FideleStructure.structure))
    )
    result = await session.exec(statement)
    items = result.all()

    return send200([FideleStructureProjShallowWithoutFideleData.model_validate(i) for i in items])


@fidele_structures_router.delete("/{id_structure}")
async def remove_fidele_structure(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele_structure: Annotated[FideleStructure, Depends(required_fidele_structure)],
) -> FideleStructureProjFlat:
    """Supprimer (soft delete) l'adhésion d'un fidèle à une structure."""

    fidele_structure.est_supprimee = True
    fidele_structure.date_suppression = datetime.now(timezone.utc)
    fidele_structure.date_modification = datetime.now(timezone.utc)

    session.add(fidele_structure)
    await session.commit()

    return send200(FideleStructureProjFlat.model_validate(fidele_structure))
