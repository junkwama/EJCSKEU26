from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db import get_session
from models.constants import Structure
from models.constants.utils import StructureBase, StructureUpdate
from models.constants.projections import StructureProjFlat, StructureProjShallow
from routers.dependencies import check_resource_exists
from routers.utils import apply_projection
from routers.utils.http_utils import send200
from utils.constants import ProjDepth

# ============================================================================
# ROUTER SETUP
# ============================================================================
structure_router = APIRouter(prefix="/structures", tags=["Constants - Structures"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_structure(
    id: Annotated[int, Path(..., description="Structure's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Structure:
    """Get and validate Structure exists"""
    return await check_resource_exists(Structure, id, session)

async def get_structure_complete_data_by_id(id: int, session: AsyncSession, proj: ProjDepth = ProjDepth.SHALLOW) -> Structure:
    statement = select(Structure).where(
       (Structure.id == id) & 
       (Structure.est_supprimee == False)
    )
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(selectinload(Structure.structure_type))
    
    result = await session.exec(statement)
    return result.first()
    
# ============================================================================
# ENDPOINTS
# ============================================================================
@structure_router.get("")
async def get_structures(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[StructureProjFlat]:
    """
    Récupérer la liste des structures disponibles

    Returns:
        Liste des structures (mouvements, associations, services)
    """
    statement = select(Structure).where(Structure.est_supprimee == False)
    result = await session.exec(statement)
    structures = result.all()
    structures_proj = [StructureProjFlat.model_validate(s) for s in structures]

    return send200(structures_proj)


@structure_router.post("")
async def create_structure(
    structure_data: StructureBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> StructureProjFlat | StructureProjShallow:
    """
    Créer une nouvelle structure

    Args:
        structure_data: Les données de la structure à créer

    Returns:
        La structure créée
    """
    structure = Structure.model_validate(structure_data, from_attributes=True)
    session.add(structure)
    await session.commit()
    await session.refresh(structure)
    
    if proj == ProjDepth.SHALLOW:
        structure = await get_structure_complete_data_by_id(structure.id, session, proj)

    projected_response = apply_projection(
        structure,
        StructureProjFlat,
        StructureProjShallow,
        proj
    )

    return send200(projected_response)


@structure_router.put("/{id}")
async def update_structure(
    structure_data: StructureUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    structure: Annotated[Structure, Depends(required_structure)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> StructureProjFlat | StructureProjShallow:
    """
    Mettre à jour une structure

    Args:
        id: ID de la structure à mettre à jour
        structure_data: Les nouvelles données de la structure

    Returns:
        La structure mise à jour
    """
    update_data = structure_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(structure, field, value)

    # Update modification timestamp
    structure.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(structure)
    await session.commit()

    if proj == ProjDepth.SHALLOW:
        structure = await get_structure_complete_data_by_id(structure.id, session, proj)

    projected_response = apply_projection(
        structure,
        StructureProjFlat,
        StructureProjShallow,
        proj
    )

    return send200(projected_response)
