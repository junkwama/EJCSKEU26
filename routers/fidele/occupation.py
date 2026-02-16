from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.constants import NiveauEtudes, Profession
from models.fidele import Fidele, FideleOccupation
from models.fidele.projection import (
    FideleOccupationProjFlat,
    FideleOccupationProjShallowWithoutFideleData,
)
from models.fidele.utils import FideleOccupationCreate, FideleOccupationUpdate
from routers.dependencies import check_resource_exists
from routers.fidele.utils import required_fidele
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send400, send404
from utils.constants import ProjDepth


fidele_occupation_router = APIRouter(prefix="/{id}/occupation", tags=["Fidele - Occupation"])


async def get_fidele_occupation_complete_data_by_fidele_id(
    fidele_id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
) -> FideleOccupation | None:
    statement = select(FideleOccupation).where(
        (FideleOccupation.id_fidele == fidele_id)
        & (FideleOccupation.est_supprimee == False)
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(FideleOccupation.niveau_etude),
            selectinload(FideleOccupation.profession),
        )

    result = await session.exec(statement)
    return result.first()


@fidele_occupation_router.post("")
async def create_fidele_occupation(
    body: FideleOccupationCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOccupationProjShallowWithoutFideleData | FideleOccupationProjFlat:
    """Créer les informations d'occupation d'un fidèle."""

    payload = body.model_dump(mode="json", exclude_unset=True)
    await check_resource_exists(NiveauEtudes, session, filters={"id": payload["id_niveau_etude"]})
    await check_resource_exists(Profession, session, filters={"id": payload["id_profession"]})

    statement = select(FideleOccupation).where(FideleOccupation.id_fidele == fidele.id)
    result = await session.exec(statement)
    existing = result.first()

    if existing and existing.est_supprimee == False:
        return send400(["path", "id"], "Les informations d'occupation existent déjà pour ce fidèle")

    if existing and existing.est_supprimee == True:
        for field, value in payload.items():
            setattr(existing, field, value)
        existing.est_supprimee = False
        existing.date_suppression = None
        existing.date_modification = datetime.now(timezone.utc)

        session.add(existing)
        await session.commit()
        await session.refresh(existing)

        if proj == ProjDepth.SHALLOW:
            existing = await get_fidele_occupation_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            existing,
            FideleOccupationProjFlat,
            FideleOccupationProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    occupation = FideleOccupation(id_fidele=fidele.id, **payload)
    session.add(occupation)
    await session.commit()
    await session.refresh(occupation)

    if proj == ProjDepth.SHALLOW:
        occupation = await get_fidele_occupation_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        occupation,
        FideleOccupationProjFlat,
        FideleOccupationProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_occupation_router.get("")
async def get_fidele_occupation(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOccupationProjShallowWithoutFideleData | FideleOccupationProjFlat | None:
    """Récupérer les informations d'occupation d'un fidèle."""

    occupation = await get_fidele_occupation_complete_data_by_fidele_id(fidele.id, session, proj)
    if not occupation:
        return send200(None)

    projected_response = apply_projection(
        occupation,
        FideleOccupationProjFlat,
        FideleOccupationProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_occupation_router.put("")
async def update_fidele_occupation(
    body: FideleOccupationUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOccupationProjShallowWithoutFideleData | FideleOccupationProjFlat:
    """Créer/mettre à jour les informations d'occupation d'un fidèle."""

    update_data = body.model_dump(mode="json", exclude_unset=True)
    await check_resource_exists(NiveauEtudes, session, filters={"id": update_data["id_niveau_etude"]})
    await check_resource_exists(Profession, session, filters={"id": update_data["id_profession"]})

    statement = select(FideleOccupation).where(FideleOccupation.id_fidele == fidele.id)
    result = await session.exec(statement)
    occupation = result.first()

    if not occupation:
        occupation = FideleOccupation(id_fidele=fidele.id, **update_data)
        session.add(occupation)
        await session.commit()
        await session.refresh(occupation)

        if proj == ProjDepth.SHALLOW:
            occupation = await get_fidele_occupation_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            occupation,
            FideleOccupationProjFlat,
            FideleOccupationProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    for field, value in update_data.items():
        setattr(occupation, field, value)

    occupation.est_supprimee = False
    occupation.date_suppression = None
    occupation.date_modification = datetime.now(timezone.utc)

    session.add(occupation)
    await session.commit()
    await session.refresh(occupation)

    if proj == ProjDepth.SHALLOW:
        occupation = await get_fidele_occupation_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        occupation,
        FideleOccupationProjFlat,
        FideleOccupationProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_occupation_router.delete("")
async def delete_fidele_occupation(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleOccupationProjFlat:
    """Supprimer les informations d'occupation d'un fidèle (soft delete)."""

    statement = select(FideleOccupation).where(
        (FideleOccupation.id_fidele == fidele.id)
        & (FideleOccupation.est_supprimee == False)
    )
    result = await session.exec(statement)
    occupation = result.first()

    if not occupation:
        return send404(["query", "id"], "Informations d'occupation non trouvées pour ce fidèle")

    occupation.est_supprimee = True
    occupation.date_suppression = datetime.now(timezone.utc)
    occupation.date_modification = datetime.now(timezone.utc)

    session.add(occupation)
    await session.commit()

    return send200(FideleOccupationProjFlat.model_validate(occupation))
