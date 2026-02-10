from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import MouvementAssociation
from models.constants.utils import MouvementAssociationBase, MouvementAssociationUpdate
from models.constants.projections import MouvementAssociationProjFlat
from models.fidele import projection
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
mouvements_router = APIRouter(prefix="/mouvements_association", tags=["Constants - Mouvements & Associations"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_mouvement_association(
    id: Annotated[int, Path(..., description="Mouvement/Association's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> MouvementAssociation:
    """Get and validate MouvementAssociation exists"""
    return await check_resource_exists(MouvementAssociation, id, session)


# ============================================================================
# ENDPOINTS
# ============================================================================
@mouvements_router.get("")
async def get_mouvements_association(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[MouvementAssociationProjFlat]:
    """
    Récupérer la liste des associations/mouvements disponibles

    Returns:
        Liste des associations/mouvements (chorale, scouts, etc.)
    """
    statement = select(MouvementAssociation).where(MouvementAssociation.est_supprimee == False)
    result = await session.exec(statement)
    mouvements = result.all()
    mouvements_proj = [MouvementAssociationProjFlat.model_validate(m) for m in mouvements]

    return send200(mouvements_proj)


@mouvements_router.post("")
async def create_mouvement_association(
    mouvement_association_data: MouvementAssociationBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> MouvementAssociationProjFlat:
    """
    Créer un nouveau mouvement/association

    Args:
        mouvement_association_data: Les données du mouvement/association à créer

    Returns:
        Le mouvement/association créé
    """
    mouvement_association = MouvementAssociation.model_validate(mouvement_association_data, from_attributes=True)
    session.add(mouvement_association)
    await session.commit()
    await session.refresh(mouvement_association)
    
    return send200(MouvementAssociationProjFlat.model_validate(mouvement_association))


@mouvements_router.put("/{id}")
async def update_mouvement_association(
    mouvement_association_data: MouvementAssociationUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    mouvement_association: Annotated[MouvementAssociation, Depends(required_mouvement_association)],
) -> MouvementAssociationProjFlat:
    """
    Mettre à jour un mouvement/association

    Args:
        id: ID du mouvement/association à mettre à jour
        mouvement_association_data: Les nouvelles données du mouvement/association

    Returns:
        Le mouvement/association mis à jour
    """
    update_data = mouvement_association_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(mouvement_association, field, value)

    # Update modification timestamp
    mouvement_association.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(mouvement_association)
    await session.commit()

    projected_response = MouvementAssociationProjFlat.model_validate(mouvement_association)
    return send200(projected_response)
