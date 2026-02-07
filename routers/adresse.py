from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from datetime import datetime, timezone

# Local modules
from core.db import get_session
from models.adresse import Adresse
from models.adresse.utils import AdresseBase, AdresseUpdate
from models.adresse.projection import AdresseProjFlat, AdresseProjShallow
from routers.utils.http_utils import send200, send404
from routers.dependencies import check_resource_exists

# ============================================================================
# ROUTER SETUP
# ============================================================================
adresse_router = APIRouter(tags=["Adresse"])


async def address_required(
    id: Annotated[int, Path(..., description="ID de l'adresse")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Adresse:
    """Get and validate Adresse exists"""
    return await check_resource_exists(Adresse, id, session)

async def get_adresse_complete_data_by_id(id: int, session: AsyncSession) -> Adresse:
    statement = (
        select(Adresse)
        .where(Adresse.id == id)
        .options(
            selectinload(Adresse.nation)
        )
    )
    result = await session.exec(statement)
    adresse = result.first()
    
    return adresse

# ============================================================================
# ENDPOINTS
# ============================================================================
@adresse_router.post("")
async def create_adresse(
    adresse_data: AdresseBase,
    session: Annotated[AsyncSession, Depends(get_session)] = None,
) -> AdresseProjShallow:
    """
    Créer une nouvelle adresse
    
    Body: AdresseBase (contient id_document_type, id_document et autres champs)
    """
    # Create adresse
    adresse = Adresse(**adresse_data.model_dump(mode='json'))
    
    session.add(adresse)
    await session.commit()
    await session.refresh(adresse)
    
    return send200(AdresseProjShallow.model_validate(adresse))


@adresse_router.get("/{id}")
async def get_adresse(
    id: Annotated[int, Path(..., description="ID de l'adresse")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AdresseProjShallow:
    """
    Récupérer une adresse par son ID
    """
    adresse = await get_adresse_complete_data_by_id(id, session)
    
    if not adresse:
        return send404(["query", "id"], "Adresse non existante")
    
    return send200(AdresseProjShallow.model_validate(adresse))


@adresse_router.put("/{id}")
async def update_adresse(
    adresse_data: AdresseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    adresse: Annotated[Adresse, Depends(address_required)],
) -> AdresseProjShallow:
    """
    Modifier une adresse existante
    """
    # Update fields
    update_data = adresse_data.model_dump(mode='json', exclude_unset=True)
    for field, value in update_data.items():
        setattr(adresse, field, value)
    
    adresse.date_modification = datetime.now(timezone.utc)
        
    session.add(adresse)
    await session.commit()
    await session.refresh(adresse)

    # Fetch the complete data with relations for the response for the Shallow Projection
    adresse_complet_data = await get_adresse_complete_data_by_id(adresse.id, session)
    
    return send200(AdresseProjShallow.model_validate(adresse_complet_data))


@adresse_router.delete("/{id}")
async def delete_adresse(
    session: Annotated[AsyncSession, Depends(get_session)],
    adresse: Annotated[Adresse, Depends(address_required)],
) -> AdresseProjFlat:
    """
    Supprimer une adresse (hard delete)
    """

    # save the adresse data for the response before deleting
    adresse_proj = AdresseProjFlat.model_validate(adresse)
    
    # Hard delete the adresse
    session.delete(adresse)
    await session.commit()
    
    return send200(adresse_proj)
