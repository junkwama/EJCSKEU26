from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import Fonction
from models.constants.utils import FonctionBase, FonctionUpdate
from models.constants.projections import FonctionProjFlat
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
fonction_router = APIRouter(prefix="/fonction", tags=["Constants - Fonctions"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_fonction(
    id: Annotated[int, Path(..., description="Fonction's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Fonction:
    """Get and validate Fonction exists"""
    return await check_resource_exists(Fonction, id, session)


# ============================================================================
# ENDPOINTS
# ============================================================================
@fonction_router.get("")
async def get_fonctions(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[FonctionProjFlat]:
    """
    Récupérer la liste des fonctions disponibles

    Returns:
        Liste des fonctions (président, secrétaire, etc.)
    """
    statement = select(Fonction).where(Fonction.est_supprimee == False)
    result = await session.exec(statement)
    fonctions = result.all()
    fonctions_proj = [FonctionProjFlat.model_validate(f) for f in fonctions]

    return send200(fonctions_proj)


@fonction_router.post("")
async def create_fonction(
    fonction_data: FonctionBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FonctionProjFlat:
    """
    Créer une nouvelle fonction

    Args:
        fonction_data: Les données de la fonction à créer

    Returns:
        La fonction créée
    """
    fonction = Fonction.model_validate(fonction_data, from_attributes=True)
    session.add(fonction)
    await session.commit()
    await session.refresh(fonction)
    
    return send200(FonctionProjFlat.model_validate(fonction))


@fonction_router.put("/{id}")
async def update_fonction(
    fonction_data: FonctionUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fonction: Annotated[Fonction, Depends(required_fonction)],
) -> FonctionProjFlat:
    """
    Mettre à jour une fonction

    Args:
        id: ID de la fonction à mettre à jour
        fonction_data: Les nouvelles données de la fonction

    Returns:
        La fonction mise à jour
    """
    update_data = fonction_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(fonction, field, value)

    # Update modification timestamp
    fonction.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(fonction)
    await session.commit()

    projected_response = FonctionProjFlat.model_validate(fonction)
    return send200(projected_response)

