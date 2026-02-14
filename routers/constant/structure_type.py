from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import StructureType
from models.constants.projections import StructureTypeProjFlat
from models.constants.utils import StructureTypeBase, StructureTypeUpdate
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
structure_type_router = APIRouter(
    prefix="/structure_type", tags=["Constants - Structure Types"]
)


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_structure_type(
    id: Annotated[int, Path(..., description="Structure Type's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> StructureType:
    """Get and validate StructureType exists"""
    return await check_resource_exists(StructureType, session, filters={"id": id})


# ============================================================================
# ENDPOINTS
# ============================================================================
@structure_type_router.get("")
async def get_structure_types(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[StructureTypeProjFlat]:
    """Récupérer les types de structures disponibles."""
    statement = select(StructureType).where(StructureType.est_supprimee == False)
    result = await session.exec(statement)
    structure_types = result.all()

    projected = [StructureTypeProjFlat.model_validate(st) for st in structure_types]
    return send200(projected)


@structure_type_router.post("")
async def create_structure_type(
    body: StructureTypeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> StructureTypeProjFlat:
    """Créer un nouveau type de structure."""
    structure_type = StructureType.model_validate(body, from_attributes=True)
    session.add(structure_type)
    await session.commit()
    await session.refresh(structure_type)

    projected = StructureTypeProjFlat.model_validate(structure_type)
    return send200(projected)


@structure_type_router.put("/{id}")
async def update_structure_type(
    body: StructureTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    structure_type: Annotated[StructureType, Depends(required_structure_type)],
) -> StructureTypeProjFlat:
    """Mettre à jour un type de structure."""
    update_data = body.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(structure_type, field, value)

    structure_type.date_modification = datetime.now(timezone.utc)

    session.add(structure_type)
    await session.commit()

    projected = StructureTypeProjFlat.model_validate(structure_type)
    return send200(projected)
