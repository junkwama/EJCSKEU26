from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from datetime import datetime, timezone

# Local modules
from core.db import get_session
from models.adresse import Adresse, Nation
from models.adresse.utils import AdresseBase, AdresseUpdate
from models.adresse.projection import AdresseProjFlat, AdresseProjShallow
from routers.utils import apply_projection, check_document_reference_exists
from routers.utils.http_utils import send200
from routers.dependencies import check_resource_exists
from utils.constants import ProjDepth

# ============================================================================
# ROUTER SETUP
# ============================================================================
adresse_router = APIRouter(tags=["Adresse"])

async def address_required(
    id: Annotated[int, Path(..., description="ID de l'adresse")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AdresseProjShallow:
    """Get and validate Adresse exists"""
    return await check_resource_exists(Adresse, session, filters={"id": id})

async def get_adresse_complete_data_by_id(id: int, session: AsyncSession) -> Adresse:
    statement = (
        select(Adresse)
        .where(Adresse.id == id)
        .options(
            selectinload(Adresse.nation)
            .selectinload(Nation.continent)
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
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Créer une nouvelle adresse
    
    Body: AdresseBase (contient id_document_type, id_document et autres champs)
    """
    await check_resource_exists(Nation, session, filters={"id": adresse_data.id_nation})
    await check_document_reference_exists(
        session,
        id_document_type=adresse_data.id_document_type,
        id_document=adresse_data.id_document,
    )

    # Create adresse
    adresse = Adresse(**adresse_data.model_dump(mode='json'))
    
    session.add(adresse)
    await session.commit()
    await session.refresh(adresse)

    # Re-fetch the adresse with relations for the Shallow Projection response
    if proj == ProjDepth.SHALLOW:
        adresse = await get_adresse_complete_data_by_id(adresse.id, session)

    projected_response = apply_projection(
        adresse,
        AdresseProjFlat,
        AdresseProjShallow,
        proj
    )
    
    return send200(projected_response)


@adresse_router.get("/{id}")
async def get_adresse(
    id: Annotated[int, Path(..., description="ID de l'adresse")],
    session: Annotated[AsyncSession, Depends(get_session)],
    adresse: Annotated[Adresse, Depends(address_required)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Récupérer une adresse par son ID
    """
    if proj == ProjDepth.SHALLOW:
        adresse = await get_adresse_complete_data_by_id(id, session)
    
    projected_response = apply_projection(
        adresse,
        AdresseProjFlat,
        AdresseProjShallow,
        proj
    )
    
    return send200(projected_response)

@adresse_router.put("/{id}")
async def update_adresse(
    adresse_data: AdresseUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    adresse: Annotated[Adresse, Depends(address_required)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> AdresseProjShallow | AdresseProjFlat:
    """
    Modifier une adresse existante
    """
    update_data = adresse_data.model_dump(mode='json', exclude_unset=True)

    if "id_nation" in update_data and update_data["id_nation"] is not None:
        await check_resource_exists(Nation, session, filters={"id": update_data["id_nation"]})

    # Update fields
    for field, value in update_data.items():
        setattr(adresse, field, value)
    
    adresse.date_modification = datetime.now(timezone.utc)
        
    session.add(adresse)
    await session.commit()
    await session.refresh(adresse)

    # Fetch the complete data with relations for the response for the Shallow Projection
    if proj == ProjDepth.SHALLOW:
        adresse = await get_adresse_complete_data_by_id(adresse.id, session)
    
    projected_response = apply_projection(
        adresse,
        AdresseProjFlat,
        AdresseProjShallow,
        proj
    )
    
    return send200(projected_response)


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
