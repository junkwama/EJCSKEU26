from datetime import datetime, timezone
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db import get_session
from models.adresse import Nation
from models.adresse.utils import NationBase, NationUpdate
from models.adresse.projection import NationProjFlat, NationProjShallow
from routers.dependencies import check_resource_exists
from routers.utils import apply_projection
from routers.utils.http_utils import send200
from utils.constants import ProjDepth

# ============================================================================
# ROUTER SETUP
# ============================================================================
nations_router = APIRouter(prefix="/nations", tags=["Constants - Nations"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_nation(
    id: Annotated[int, Path(..., description="Nation's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Nation:
    """Get and validate Nation exists"""
    return await check_resource_exists(Nation, id, session)

async def get_nation_complete_data_by_id(
    id: int, 
    session: AsyncSession, 
    proj: ProjDepth = ProjDepth.SHALLOW
) -> Nation:

    statement = select(Nation).where(Nation.id == id)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(selectinload(Nation.continent))
        
    result = await session.exec(statement)
    nation = result.first()
    
    return nation

# ============================================================================
# ENDPOINTS
# ============================================================================
@nations_router.get("")
async def get_nations(
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> List[Union[NationProjFlat, NationProjShallow]]:
    """
    Récupérer la liste des nations disponibles

    Returns:
        Liste des nations disponibles pour les adresses
    """
    statement = select(Nation)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(selectinload(Nation.continent))
    
    result = await session.exec(statement)
    nations = result.all()
    
    projected_nations = [
        apply_projection(nation, NationProjFlat, NationProjShallow, proj)
        for nation in nations
    ]

    return send200(projected_nations)


@nations_router.post("")
async def create_nation(
    nation_data: NationBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> NationProjShallow | NationProjFlat:
    """
    Créer une nouvelle nation

    Args:
        nation_data: Les données de la nation à créer

    Returns:
        La nation créée avec ses relations
    """
    nation = Nation.model_validate(nation_data, from_attributes=True)
    session.add(nation)
    await session.commit()
    
    # Reload with relationship
    if proj == ProjDepth.SHALLOW:
        nation = await get_nation_complete_data_by_id(nation.id, session, proj)
    else:
        await session.refresh(nation)

    projected_response = apply_projection(nation, NationProjFlat, NationProjShallow, proj)
    return send200(projected_response)

@nations_router.put("/{id}")
async def update_nation(
    nation_data: NationUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    nation: Annotated[Nation, Depends(required_nation)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> NationProjShallow | NationProjFlat:
    """
    Mettre à jour une nation

    Args:
        id: ID de la nation à mettre à jour
        nation_data: Les nouvelles données de la nation

    Returns:
        La nation mise à jour avec ses relations
    """
    update_data = nation_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(nation, field, value)

    # Update modification timestamp
    nation.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(nation)
    await session.commit()

    if proj == ProjDepth.SHALLOW:
        nation = await get_nation_complete_data_by_id(nation.id, session, proj)
    else:
        await session.refresh(nation)

    projected_response = apply_projection(nation, NationProjFlat, NationProjShallow, proj)
    return send200(projected_response)

