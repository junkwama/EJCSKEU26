from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import FideleType
from models.constants.utils import FideleTypeBase, FideleTypeUpdate
from models.constants.projections import FideleTypeProjFlat
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
fidele_types_router = APIRouter(prefix="/fidele_types", tags=["Constants - Fidele Types"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_fidele_type(
    id: Annotated[int, Path(..., description="Fidele Type's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleType:
    """Get and validate FideleType exists"""
    return await check_resource_exists(FideleType, id, session)


# ============================================================================
# ENDPOINTS
# ============================================================================
@fidele_types_router.get("")
async def get_fidele_types(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[FideleTypeProjFlat]:
    """
    Récupérer les types de fidèles disponibles

    Returns:
        Liste des types de fidèles (Pratiquant, Sympathisant, etc.)
    """
    statement = select(FideleType).where(FideleType.est_supprimee == False)
    result = await session.exec(statement)
    fidele_types = result.all()
    fidele_types_proj = [FideleTypeProjFlat.model_validate(ft) for ft in fidele_types]

    return send200(fidele_types_proj)


@fidele_types_router.post("")
async def create_fidele_type(
    fidele_type_data: FideleTypeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleTypeProjFlat:
    """
    Créer un nouveau type de fidèle

    Args:
        fidele_type_data: Les données du type de fidèle à créer

    Returns:
        Le type de fidèle créé
    """
    fidele_type = FideleType.model_validate(fidele_type_data, from_attributes=True)
    session.add(fidele_type)
    await session.commit()
    await session.refresh(fidele_type)

    return send200(FideleTypeProjFlat.model_validate(fidele_type))


@fidele_types_router.put("/{id}")
async def update_fidele_type(
    fidele_type_data: FideleTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele_type: Annotated[FideleType, Depends(required_fidele_type)],
) -> FideleTypeProjFlat:
    """
    Mettre à jour un type de fidèle

    Args:
        id: ID du type de fidèle à mettre à jour
        fidele_type_data: Les nouvelles données du type de fidèle

    Returns:
        Le type de fidèle mis à jour
    """

    # Update fields (only provided fields)
    update_data = fidele_type_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(fidele_type, field, value)

    # Update modification timestamp
    fidele_type.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(fidele_type)
    await session.commit()

    projected_response = FideleTypeProjFlat.model_validate(fidele_type)
    return send200(projected_response)