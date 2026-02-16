from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.adresse import Nation
from models.fidele import Fidele, FideleOrigine
from models.fidele.projection import FideleOrigineProjFlat, FideleOrigineProjShallowWithoutFideleData
from models.fidele.utils import FideleOrigineUpdate
from routers.dependencies import check_resource_exists
from routers.fidele.utils import required_fidele
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send400, send404
from utils.constants import ProjDepth


fidele_origine_router = APIRouter(prefix="/{id}/origine", tags=["Fidele - Origine"])


async def get_fidele_origine_complete_data_by_fidele_id(
    fidele_id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
) -> FideleOrigine | None:
    statement = select(FideleOrigine).where(
        (FideleOrigine.id_fidele == fidele_id)
        & (FideleOrigine.est_supprimee == False)
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(selectinload(FideleOrigine.nation))

    result = await session.exec(statement)
    return result.first()

@fidele_origine_router.post("")
async def create_fidele_origine(
    body: FideleOrigineUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOrigineProjShallowWithoutFideleData | FideleOrigineProjFlat:
    """Créer les informations d'origine d'un fidèle."""

    payload = body.model_dump(mode="json", exclude_unset=True)
    if "id_nation" in payload and payload["id_nation"] is not None:
        await check_resource_exists(Nation, session, filters={"id": payload["id_nation"]})

    statement = select(FideleOrigine).where(FideleOrigine.id_fidele == fidele.id)
    result = await session.exec(statement)
    existing = result.first()

    if existing and existing.est_supprimee == False:
        return send400(["path", "id"], "Les informations d'origine existent déjà pour ce fidèle")

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
            existing = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            existing,
            FideleOrigineProjFlat,
            FideleOrigineProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    origine = FideleOrigine(id_fidele=fidele.id, **payload)
    session.add(origine)
    await session.commit()
    await session.refresh(origine)

    if proj == ProjDepth.SHALLOW:
        origine = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        origine,
        FideleOrigineProjFlat,
        FideleOrigineProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_origine_router.get("")
async def get_fidele_origine(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOrigineProjShallowWithoutFideleData | FideleOrigineProjFlat | None:
    """Récupérer les informations d'origine d'un fidèle."""

    origine = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, proj)
    if not origine:
        return send200(None)

    projected_response = apply_projection(
        origine,
        FideleOrigineProjFlat,
        FideleOrigineProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_origine_router.put("")
async def update_fidele_origine(
    body: FideleOrigineUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleOrigineProjShallowWithoutFideleData | FideleOrigineProjFlat:
    """Créer/mettre à jour les informations d'origine d'un fidèle."""

    update_data = body.model_dump(mode="json", exclude_unset=True)
    if "id_nation" in update_data and update_data["id_nation"] is not None:
        await check_resource_exists(Nation, session, filters={"id": update_data["id_nation"]})

    statement = select(FideleOrigine).where(FideleOrigine.id_fidele == fidele.id)
    result = await session.exec(statement)
    origine = result.first()

    if not origine:
        origine = FideleOrigine(id_fidele=fidele.id, **update_data)
        session.add(origine)
        await session.commit()
        await session.refresh(origine)

        if proj == ProjDepth.SHALLOW:
            origine = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            origine,
            FideleOrigineProjFlat,
            FideleOrigineProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    for field, value in update_data.items():
        setattr(origine, field, value)

    origine.est_supprimee = False
    origine.date_suppression = None
    origine.date_modification = datetime.now(timezone.utc)

    session.add(origine)
    await session.commit()
    await session.refresh(origine)

    if proj == ProjDepth.SHALLOW:
        origine = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        origine,
        FideleOrigineProjFlat,
        FideleOrigineProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_origine_router.delete("")
async def delete_fidele_origine(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleOrigineProjFlat:
    """Supprimer les informations d'origine d'un fidèle (soft delete)."""

    origine = await get_fidele_origine_complete_data_by_fidele_id(fidele.id, session, ProjDepth.FLAT)
    if not origine:
        return send404(["query", "id"], "Informations d'origine non trouvées pour ce fidèle")

    origine.est_supprimee = True
    origine.date_suppression = datetime.now(timezone.utc)
    origine.date_modification = datetime.now(timezone.utc)

    session.add(origine)
    await session.commit()

    return send200(FideleOrigineProjFlat.model_validate(origine))
