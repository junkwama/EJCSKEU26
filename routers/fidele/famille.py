from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.fidele import Fidele, FideleFamille
from models.fidele.projection import FideleFamilleProjFlat
from models.fidele.utils import FideleFamilleBase, FideleFamilleUpdate
from routers.fidele.utils import required_fidele
from routers.utils.http_utils import send200, send400, send404


fidele_famille_router = APIRouter(prefix="/{id}/famille", tags=["Fidele - Famille"])


async def get_fidele_famille_by_fidele_id(fidele_id: int, session: AsyncSession) -> FideleFamille | None:
    statement = select(FideleFamille).where(
        (FideleFamille.id_fidele == fidele_id)
        & (FideleFamille.est_supprimee == False)
    )
    result = await session.exec(statement)
    return result.first()


@fidele_famille_router.post("")
async def create_fidele_famille(
    body: FideleFamilleBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleFamilleProjFlat:
    """Créer les informations familiales d'un fidèle."""

    payload = body.model_dump(mode="json", exclude_unset=True)

    statement = select(FideleFamille).where(FideleFamille.id_fidele == fidele.id)
    result = await session.exec(statement)
    existing = result.first()

    if existing and existing.est_supprimee == False:
        return send400(["path", "id"], "Les informations familiales existent déjà pour ce fidèle")

    if existing and existing.est_supprimee == True:
        for field, value in payload.items():
            setattr(existing, field, value)
        existing.est_supprimee = False
        existing.date_suppression = None
        existing.date_modification = datetime.now(timezone.utc)

        session.add(existing)
        await session.commit()
        await session.refresh(existing)
        return send200(FideleFamilleProjFlat.model_validate(existing))

    famille = FideleFamille(id_fidele=fidele.id, **payload)
    session.add(famille)
    await session.commit()
    await session.refresh(famille)

    return send200(FideleFamilleProjFlat.model_validate(famille))


@fidele_famille_router.get("")
async def get_fidele_famille(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleFamilleProjFlat | None:
    """Récupérer les informations familiales d'un fidèle."""

    famille = await get_fidele_famille_by_fidele_id(fidele.id, session)
    if not famille:
        return send200(None)

    return send200(FideleFamilleProjFlat.model_validate(famille))


@fidele_famille_router.put("")
async def update_fidele_famille(
    body: FideleFamilleUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleFamilleProjFlat:
    """Créer/mettre à jour les informations familiales d'un fidèle."""

    update_data = body.model_dump(mode="json", exclude_unset=True)

    statement = select(FideleFamille).where(FideleFamille.id_fidele == fidele.id)
    result = await session.exec(statement)
    famille = result.first()

    if not famille:
        famille = FideleFamille(id_fidele=fidele.id, **update_data)
        session.add(famille)
        await session.commit()
        await session.refresh(famille)
        return send200(FideleFamilleProjFlat.model_validate(famille))

    for field, value in update_data.items():
        setattr(famille, field, value)

    famille.est_supprimee = False
    famille.date_suppression = None
    famille.date_modification = datetime.now(timezone.utc)

    session.add(famille)
    await session.commit()
    await session.refresh(famille)

    return send200(FideleFamilleProjFlat.model_validate(famille))


@fidele_famille_router.delete("")
async def delete_fidele_famille(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FideleFamilleProjFlat:
    """Supprimer les informations familiales d'un fidèle (soft delete)."""

    famille = await get_fidele_famille_by_fidele_id(fidele.id, session)
    if not famille:
        return send404(["query", "id"], "Informations familiales non trouvées pour ce fidèle")

    famille.est_supprimee = True
    famille.date_suppression = datetime.now(timezone.utc)
    famille.date_modification = datetime.now(timezone.utc)

    session.add(famille)
    await session.commit()

    return send200(FideleFamilleProjFlat.model_validate(famille))
