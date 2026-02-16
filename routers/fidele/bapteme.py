from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.fidele import Fidele, FideleBapteme
from models.fidele.projection import FideleBaptemeProjFlat, FideleBaptemeProjShallowWithoutFideleData
from models.fidele.utils import FideleBaptemeUpdate
from models.paroisse import Paroisse
from routers.dependencies import check_resource_exists
from routers.fidele.utils import required_fidele
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send400, send404
from utils.constants import ProjDepth


fidele_bapteme_router = APIRouter(prefix="/{id}/bapteme", tags=["Fidele - Bapteme"])


async def get_fidele_bapteme_complete_data_by_fidele_id(
    fidele_id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
) -> FideleBapteme | None:
    statement = select(FideleBapteme).where(
        (FideleBapteme.id_fidele == fidele_id)
        & (FideleBapteme.est_supprimee == False)
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(selectinload(FideleBapteme.paroisse))

    result = await session.exec(statement)
    return result.first()

@fidele_bapteme_router.post("")
async def create_fidele_bapteme(
    body: FideleBaptemeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleBaptemeProjShallowWithoutFideleData | FideleBaptemeProjFlat:
    """Créer les informations de baptême d'un fidèle."""

    payload = body.model_dump(mode="json", exclude_unset=True)
    if "id_paroisse" in payload and payload["id_paroisse"] is not None:
        await check_resource_exists(Paroisse, session, filters={"id": payload["id_paroisse"]})

    statement = select(FideleBapteme).where(FideleBapteme.id_fidele == fidele.id)
    result = await session.exec(statement)
    existing = result.first()

    if existing and existing.est_supprimee == False:
        return send400(["path", "id"], "Les informations de baptême existent déjà pour ce fidèle")

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
            existing = await get_fidele_bapteme_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            existing,
            FideleBaptemeProjFlat,
            FideleBaptemeProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    bapteme = FideleBapteme(id_fidele=fidele.id, **payload)
    session.add(bapteme)
    await session.commit()
    await session.refresh(bapteme)

    if proj == ProjDepth.SHALLOW:
        bapteme = await get_fidele_bapteme_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        bapteme,
        FideleBaptemeProjFlat,
        FideleBaptemeProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_bapteme_router.get("")
async def get_fidele_bapteme(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleBaptemeProjShallowWithoutFideleData | FideleBaptemeProjFlat | None:
    """Récupérer les informations de baptême d'un fidèle."""

    bapteme = await get_fidele_bapteme_complete_data_by_fidele_id(fidele.id, session, proj)
    if not bapteme:
        return send200(None)

    projected_response = apply_projection(
        bapteme,
        FideleBaptemeProjFlat,
        FideleBaptemeProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_bapteme_router.put("")
async def update_fidele_bapteme(
    body: FideleBaptemeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleBaptemeProjShallowWithoutFideleData | FideleBaptemeProjFlat:
    """Créer/mettre à jour les informations de baptême d'un fidèle."""

    update_data = body.model_dump(mode="json", exclude_unset=True)
    if "id_paroisse" in update_data and update_data["id_paroisse"] is not None:
        await check_resource_exists(Paroisse, session, filters={"id": update_data["id_paroisse"]})

    statement = select(FideleBapteme).where(FideleBapteme.id_fidele == fidele.id)
    result = await session.exec(statement)
    bapteme = result.first()

    if not bapteme:
        bapteme = FideleBapteme(id_fidele=fidele.id, **update_data)
        session.add(bapteme)
        await session.commit()
        await session.refresh(bapteme)

        if proj == ProjDepth.SHALLOW:
            bapteme = await get_fidele_bapteme_complete_data_by_fidele_id(fidele.id, session, proj)

        projected_response = apply_projection(
            bapteme,
            FideleBaptemeProjFlat,
            FideleBaptemeProjShallowWithoutFideleData,
            proj,
        )
        return send200(projected_response)

    for field, value in update_data.items():
        setattr(bapteme, field, value)

    bapteme.est_supprimee = False
    bapteme.date_suppression = None
    bapteme.date_modification = datetime.now(timezone.utc)

    session.add(bapteme)
    await session.commit()
    await session.refresh(bapteme)

    if proj == ProjDepth.SHALLOW:
        bapteme = await get_fidele_bapteme_complete_data_by_fidele_id(fidele.id, session, proj)

    projected_response = apply_projection(
        bapteme,
        FideleBaptemeProjFlat,
        FideleBaptemeProjShallowWithoutFideleData,
        proj,
    )
    return send200(projected_response)


@fidele_bapteme_router.delete("")
async def delete_fidele_bapteme(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleBaptemeProjFlat:
    """Supprimer les informations de baptême d'un fidèle (soft delete)."""

    statement = select(FideleBapteme).where(
        (FideleBapteme.id_fidele == fidele.id)
        & (FideleBapteme.est_supprimee == False)
    )
    result = await session.exec(statement)
    bapteme = result.first()

    if not bapteme:
        return send404(["query", "id"], "Informations de baptême non trouvées pour ce fidèle")

    bapteme.est_supprimee = True
    bapteme.date_suppression = datetime.now(timezone.utc)
    bapteme.date_modification = datetime.now(timezone.utc)

    session.add(bapteme)
    await session.commit()

    return send200(FideleBaptemeProjFlat.model_validate(bapteme))
