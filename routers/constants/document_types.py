from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import DocumentType
from models.constants.utils import DocumentTypeBase, DocumentTypeUpdate
from models.constants.projections import DocumentTypeProjFlat
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
document_types_router = APIRouter(prefix="/types_document", tags=["Constants - Document Types"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_document_type(
    id: Annotated[int, Path(..., description="Document Type's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentType:
    """Get and validate DocumentType exists"""
    return await check_resource_exists(DocumentType, id, session)


# ============================================================================
# ENDPOINTS
# ============================================================================
@document_types_router.get("")
async def get_document_types(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[DocumentTypeProjFlat]:
    """
    Récupérer les types de documents disponibles (FIDELE, PAROISSE, STRUCTURE)

    Returns:
        Liste des types de documents disponibles
    """
    statement = select(DocumentType)
    result = await session.exec(statement)
    document_types = result.all()
    document_types_proj = [DocumentTypeProjFlat.model_validate(dt) for dt in document_types]

    return send200(document_types_proj)


@document_types_router.post("")
async def create_document_type(
    document_type_data: DocumentTypeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentTypeProjFlat:
    """
    Créer un nouveau type de document

    Args:
        document_type_data: Les données du type de document à créer

    Returns:
        Le type de document créé
    """
    document_type = DocumentType.model_validate(document_type_data, from_attributes=True)
    session.add(document_type)
    await session.commit()
    await session.refresh(document_type)

    return send200(DocumentTypeProjFlat.model_validate(document_type))


@document_types_router.put("/{id}")
async def update_document_type(
    document_type_data: DocumentTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    document_type: Annotated[DocumentType, Depends(required_document_type)],
) -> DocumentTypeProjFlat:
    """
    Mettre à jour un type de document

    Args:
        id: ID du type de document à mettre à jour
        document_type_data: Les nouvelles données du type de document

    Returns:
        Le type de document mis à jour
    """
    # Update fields (only provided fields)
    update_data = document_type_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(document_type, field, value)

    # Update modification timestamp
    document_type.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(document_type)
    await session.commit()

    projected_response = DocumentTypeProjFlat.model_validate(document_type)
    return send200(projected_response)