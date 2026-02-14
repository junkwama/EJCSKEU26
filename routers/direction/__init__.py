from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import Config
from core.db import get_session
from models.constants import Structure
from models.direction import Direction
from models.direction.projection import DirectionProjFlat, DirectionProjShallow
from models.direction.utils import DirectionBase, DirectionUpdate
from models.direction.fonction import DirectionFonction
from routers.dependencies import check_resource_exists
from routers.direction.docs import DIRECTION_CREATE_DESCRIPTION
from routers.utils import (
    apply_projection,
    check_document_reference_exists,
    resolve_document_reference,
    resolve_document_references_batch,
)
from routers.utils.http_utils import send200, send404
from utils.constants import ProjDepth


direction_router = APIRouter()


async def required_direction(
    id: Annotated[int, Path(..., description="Direction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Direction:
    return await check_resource_exists(Direction, session, filters={"id": id})


async def get_direction_any_by_id(direction_id: int, session: AsyncSession) -> Direction | None:
    statement = select(Direction).where(Direction.id == direction_id)
    result = await session.exec(statement)
    return result.first()


async def get_direction_complete_data_by_id(
    direction_id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
) -> Direction | None:
    statement = select(Direction).where(Direction.id == direction_id)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Direction.structure).selectinload(Structure.structure_type)
        )

    result = await session.exec(statement)
    return result.first()


@direction_router.post(
    "",
    tags=["Direction"],
    summary="Créer une direction (instance dirigeante d'une structure)",
    description=DIRECTION_CREATE_DESCRIPTION,
)
async def create_direction(
    body: DirectionBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> DirectionProjShallow | DirectionProjFlat:
    """Créer une direction."""

    await check_resource_exists(Structure, session, filters={"id": body.id_structure})
    await check_document_reference_exists(
        session,
        id_document_type=body.id_document_type,
        id_document=body.id_document,
    )

    direction = Direction(**body.model_dump(mode="json"))

    session.add(direction)
    await session.commit()
    await session.refresh(direction)

    if proj == ProjDepth.SHALLOW:
        direction = await get_direction_complete_data_by_id(direction.id, session, proj)

    projected = apply_projection(direction, DirectionProjFlat, DirectionProjShallow, proj)
    if proj == ProjDepth.SHALLOW and direction is not None:
        projected.document = await resolve_document_reference(
            session,
            id_document_type=direction.id_document_type,
            id_document=direction.id_document,
        )

    return send200(projected)


@direction_router.get("", tags=["Direction"])
async def get_directions(
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.FLAT,
    offset: int = 0,
    limit: int = Query(
        Config.PREVIEW_LIST_ITEM_NUMBER.value, ge=1, le=Config.MAX_ITEMS_PER_PAGE.value
    ),
) -> List[DirectionProjFlat] | List[DirectionProjShallow]:
    """Lister les directions (soft-delete filtré)."""

    statement = select(Direction).where(Direction.est_supprimee == False)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Direction.structure).selectinload(Structure.structure_type)
        )

    statement = statement.offset(offset).limit(limit)
    result = await session.exec(statement)
    directions = result.all()

    projected_directions = [
        apply_projection(d, DirectionProjFlat, DirectionProjShallow, proj)
        for d in directions
    ]

    if proj == ProjDepth.SHALLOW:
        refs = [(d.id_document_type, d.id_document) for d in directions]
        docs = await resolve_document_references_batch(session, refs)
        for d, projected in zip(directions, projected_directions):
            key = (int(d.id_document_type), int(d.id_document))
            if hasattr(projected, "document"):
                projected.document = docs.get(key)

    return send200(projected_directions)


@direction_router.get("/{id}", tags=["Direction"])
async def get_direction(
    id: Annotated[int, Path(..., description="Direction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
    direction: Annotated[Direction, Depends(required_direction)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> DirectionProjShallow | DirectionProjFlat:
    """Récupérer une direction par ID."""

    if proj == ProjDepth.SHALLOW:
        direction = await get_direction_complete_data_by_id(id, session, proj)

    projected = apply_projection(direction, DirectionProjFlat, DirectionProjShallow, proj)
    if proj == ProjDepth.SHALLOW and direction is not None:
        projected.document = await resolve_document_reference(
            session,
            id_document_type=direction.id_document_type,
            id_document=direction.id_document,
        )

    return send200(projected)


@direction_router.put("/{id}")
async def update_direction(
    body: DirectionUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    direction: Annotated[Direction, Depends(required_direction)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> DirectionProjShallow | DirectionProjFlat:
    """Modifier une direction existante."""

    update_data = body.model_dump(mode="json", exclude_unset=True)

    # Validate foreign keys when present
    if "id_structure" in update_data and update_data["id_structure"] is not None:
        await check_resource_exists(Structure, session, filters={"id": update_data["id_structure"]})

    # Validate polymorphic document reference if either component changes
    if ("id_document_type" in update_data) or ("id_document" in update_data):
        new_id_document_type = update_data.get("id_document_type", direction.id_document_type)
        new_id_document = update_data.get("id_document", direction.id_document)
        await check_document_reference_exists(
            session,
            id_document_type=new_id_document_type,
            id_document=new_id_document,
        )

    for field, value in update_data.items():
        setattr(direction, field, value)

    direction.date_modification = datetime.now(timezone.utc)

    session.add(direction)
    await session.commit()

    if proj == ProjDepth.SHALLOW:
        direction = await get_direction_complete_data_by_id(direction.id, session, proj)

    projected = apply_projection(direction, DirectionProjFlat, DirectionProjShallow, proj)
    if proj == ProjDepth.SHALLOW and direction is not None:
        projected.document = await resolve_document_reference(
            session,
            id_document_type=direction.id_document_type,
            id_document=direction.id_document,
        )
    
    return send200(projected)


@direction_router.put("/{id}/restore", tags=["Direction"])
async def restore_direction(
    id: Annotated[int, Path(..., description="Direction ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> DirectionProjShallow | DirectionProjFlat:
    """Restaurer une direction supprimée (soft delete)."""

    direction = await get_direction_any_by_id(id, session)
    if not direction:
        return send404(["path", "id"], "Direction non trouvée")

    if direction.est_supprimee:
        direction.est_supprimee = False
        direction.date_suppression = None
        direction.date_modification = datetime.now(timezone.utc)

        session.add(direction)
        await session.commit()

    if proj == ProjDepth.SHALLOW:
        direction = await get_direction_complete_data_by_id(direction.id, session, proj)

    projected = apply_projection(direction, DirectionProjFlat, DirectionProjShallow, proj)
    if proj == ProjDepth.SHALLOW and direction is not None:
        projected.document = await resolve_document_reference(
            session,
            id_document_type=direction.id_document_type,
            id_document=direction.id_document,
        )

    return send200(projected)


@direction_router.delete("/{id}", tags=["Direction"])
async def delete_direction(
    session: Annotated[AsyncSession, Depends(get_session)],
    direction: Annotated[Direction, Depends(required_direction)],
) -> DirectionProjFlat:
    """Soft delete une direction."""

    direction.est_supprimee = True
    direction.date_suppression = datetime.now(timezone.utc)
    direction.date_modification = datetime.now(timezone.utc)

    # Cascade soft-delete: toutes les affectations (direction_fonction) de cette direction
    statement = select(DirectionFonction).where(
        (DirectionFonction.id_direction == direction.id)
        & (DirectionFonction.est_supprimee == False)
    )
    result = await session.exec(statement)
    items = result.all()
    now = datetime.now(timezone.utc)
    for item in items:
        item.est_supprimee = True
        item.date_suppression = now
        item.date_modification = now
        item.est_actif = False
        session.add(item)

    session.add(direction)
    await session.commit()

    return send200(DirectionProjFlat.model_validate(direction))


# ========================== DIRECTION_FONCTION ENDPOINTS ==========================
from routers.direction.fonctions import direction_fonctions_router

direction_router.include_router(direction_fonctions_router, tags=["Direction - Fonctions"])
