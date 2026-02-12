from __future__ import annotations

from typing import Any, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from routers.dependencies import check_resource_exists
from utils.constants import ProjDepth

P = TypeVar('P', bound=BaseModel)

def apply_projection(
    data: object,
    FlatProjection: Type[P],
    ShallowProjection: Type[P],
    proj_type: ProjDepth = ProjDepth.SHALLOW,
) -> P:
    """
    Generic function to select between flat and shallow projections
    
    Args:
        data: SQLModel instance to convert
        FlatProjection: Flat projection class
        ShallowProjection: Shallow projection class
        proj_type: "flat" or "shallow" (default: "shallow")
    
    Returns:
        Projection instance of appropriate type

    """
    
    projection_class = FlatProjection if proj_type == ProjDepth.FLAT else ShallowProjection
    return projection_class.model_validate(data)


async def check_document_reference_exists(
    session: AsyncSession,
    *,
    id_document_type: Any,
    id_document: int,
) -> SQLModel:
    """Validate a polymorphic (id_document_type, id_document) reference.

    - `id_document_type` is validated with `DocumentTypeEnum` (no DB query).
    - Existence is checked with ONE query via `check_resource_exists()`.
    """

    # Lazy import to avoid circular imports
    from models.constants.types import DocumentTypeEnum

    try:
        doc_type = (
            id_document_type
            if isinstance(id_document_type, DocumentTypeEnum)
            else DocumentTypeEnum(int(id_document_type))
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=422,
            detail=f"Invalid id_document_type={id_document_type!r}",
        ) from e

    model = _model_for_document_type(doc_type)
    if model is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported document type: {doc_type.name}({int(doc_type)})",
        )

    try:
        return await check_resource_exists(model, session, filters={"id": id_document})
    except HTTPException as e:
        if e.status_code != 404:
            raise
        raise HTTPException(
            status_code=404,
            detail=(
                f"Target document not found: type={doc_type.name}({int(doc_type)}), id={id_document}"
            ),
        ) from e


def _model_for_document_type(doc_type: Any) -> type[SQLModel] | None:
    """Map DocumentTypeEnum to its SQLModel class."""

    from models.constants.types import DocumentTypeEnum

    if doc_type == DocumentTypeEnum.FIDELE:
        from models.fidele import Fidele

        return Fidele

    if doc_type == DocumentTypeEnum.PAROISSE:
        from models.paroisse import Paroisse

        return Paroisse

    if doc_type == DocumentTypeEnum.STRUCTURE:
        from models.constants import Structure

        return Structure

    if doc_type == DocumentTypeEnum.NATION:
        from models.adresse import Nation

        return Nation

    if doc_type == DocumentTypeEnum.CONTINENT:
        from models.adresse import Continent

        return Continent

    return None
