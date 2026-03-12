from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import DocumentType
from models.constants.utils import DocumentTypeBase, DocumentTypeUpdate
from models.constants.projections import DocumentTypeProjFlat
from routers.utils import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
document_type_router = APIRouter(prefix="/types_document", tags=["Constants - Document Types"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_document_type(
    id: Annotated[int, Path(..., description="Document Type's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentType:
    """Get and validate DocumentType exists"""
    return await check_resource_exists(DocumentType, session, filters={"id": id})


# ============================================================================
# ENDPOINTS
# ============================================================================
@document_type_router.get("")
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


@document_type_router.post("")
async def create_document_type(
    body: DocumentTypeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentTypeProjFlat:
    """
    Créer un nouveau type de document

    Args:
        body: Les données du type de document à créer

    Returns:
        Le type de document créé
    """
    if body.id_document_type_superieur is not None:
        await check_resource_exists(
            DocumentType,
            session,
            filters={"id": body.id_document_type_superieur},
        )

    document_type = DocumentType.model_validate(body, from_attributes=True)
    session.add(document_type)
    await session.commit()
    await session.refresh(document_type)

    return send200(DocumentTypeProjFlat.model_validate(document_type))


@document_type_router.put("/{id}")
async def update_document_type(
    body: DocumentTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    document_type: Annotated[DocumentType, Depends(required_document_type)],
) -> DocumentTypeProjFlat:
    """
    Mettre à jour un type de document

    Args:
        id: ID du type de document à mettre à jour
        body: Les nouvelles données du type de document

    Returns:
        Le type de document mis à jour
    """
    # Update fields (only provided fields)
    update_data = body.model_dump(mode="json", exclude_unset=True)

    if "id_document_type_superieur" in update_data:
        superior_id = update_data["id_document_type_superieur"]
        if superior_id is not None:
            if superior_id == document_type.id:
                raise HTTPException(
                    status_code=422,
                    detail="id_document_type_superieur cannot reference itself",
                )
            await check_resource_exists(DocumentType, session, filters={"id": superior_id})

    for field, value in update_data.items():
        setattr(document_type, field, value)

    # Update modification timestamp
    document_type.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(document_type)
    await session.commit()

    projected_response = DocumentTypeProjFlat.model_validate(document_type)
    return send200(projected_response)