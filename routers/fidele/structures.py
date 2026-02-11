from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from core.db import get_session
from models.constants import Structure
from models.fidele import Fidele, FideleStructure
from models.fidele.utils import FideleStructureUpdate, FideleStructureCreate
from models.fidele.projection import (
    FideleStructureProjFlat,
    FideleStructureProjShallowWithStructureData,
)
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200, send400
from routers.fidele.utils import required_fidele

fidele_structures_router = APIRouter(prefix="/{id}/structure", tags=["Fidele - Structures"])


def are_membership_dates_valid(date_adhesion: date | None, date_sortie: date | None) -> bool:
    if date_adhesion and date_sortie and date_sortie < date_adhesion:
        return False
    return True


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

@fidele_structures_router.post("")
async def add_fidele_structure(
    body: FideleStructureCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleStructureProjShallowWithStructureData:
    """Ajouter une structure à un fidèle (crée une adhésion dans fidele_structure)."""

    # Ensure structure exists
    await check_resource_exists(Structure, session, filters={"id": body.id_structure})

    if not are_membership_dates_valid(body.date_adhesion, body.date_sortie):
        return send400(["body"], "Dates d'adhésion/sortie invalides")

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
        if not are_membership_dates_valid(body.date_adhesion, body.date_sortie):
            return send400(["body"], "Dates d'adhésion/sortie invalides")

        existing.est_supprimee = False
        existing.date_suppression = None
        existing.date_adhesion = body.date_adhesion
        existing.date_sortie = body.date_sortie
        existing.date_modification = datetime.now(timezone.utc)

        session.add(existing)
        await session.commit()
        await session.refresh(existing)

        existing = await get_fidele_structure_complete_data_by_id(existing.id, session)

        return send200(FideleStructureProjShallowWithStructureData.model_validate(existing))

    fidele_structure = FideleStructure(
        id_fidele=fidele.id,
        id_structure=body.id_structure,
        date_adhesion=body.date_adhesion,
        date_sortie=body.date_sortie,
    )

    session.add(fidele_structure)
    await session.commit()
    await session.refresh(fidele_structure)

    fidele_structure = await get_fidele_structure_complete_data_by_id(fidele_structure.id, session)

    return send200(FideleStructureProjShallowWithStructureData.model_validate(fidele_structure))


@fidele_structures_router.get("")
async def list_fidele_structures(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> List[FideleStructureProjShallowWithStructureData]:
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

    return send200([FideleStructureProjShallowWithStructureData.model_validate(i) for i in items])


@fidele_structures_router.put("/{id_structure}")
async def update_fidele_structure(
    body: FideleStructureUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele_structure: Annotated[FideleStructure, Depends(required_fidele_structure)],
) -> FideleStructureProjFlat:
    """Mettre à jour les dates d'adhésion/sortie d'un fidèle dans une structure."""

    update_data = body.model_dump(mode="json", exclude_unset=True)

    effective_date_adhesion = update_data.get("date_adhesion", fidele_structure.date_adhesion)
    effective_date_sortie = update_data.get("date_sortie", fidele_structure.date_sortie)
    if not are_membership_dates_valid(effective_date_adhesion, effective_date_sortie):
        return send400(["body"], "Dates d'adhésion/sortie invalides")

    for field, value in update_data.items():
        setattr(fidele_structure, field, value)

    fidele_structure.date_modification = datetime.now(timezone.utc)

    session.add(fidele_structure)
    await session.commit()
    await session.refresh(fidele_structure)

    return send200(FideleStructureProjFlat.model_validate(fidele_structure))


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
