from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from routers.dependencies import check_resource_exists
from utils.constants import ProjDepth

if TYPE_CHECKING:
    from models.constants.types import DocumentTypeEnum

P = TypeVar('P', bound=BaseModel)


def _coerce_document_type(raw_document_type: Any) -> DocumentTypeEnum | None:
    """Coerce a raw document type value into DocumentTypeEnum.

    Accepts either an enum instance or something int-castable.
    Returns None when the value is invalid/unsupported.

    Kept as a helper to avoid repeating the same coercion logic in multiple resolvers.
    """

    from models.constants.types import DocumentTypeEnum

    try:
        if isinstance(raw_document_type, DocumentTypeEnum):
            return raw_document_type
        return DocumentTypeEnum(int(raw_document_type))
    except Exception:
        return None

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

    document_type = _coerce_document_type(id_document_type)
    if document_type is None:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid id_document_type={id_document_type!r}",
        )

    model = _model_for_document_type(document_type)
    if model is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported document type: {document_type.name}({int(document_type)})",
        )

    try:
        return await check_resource_exists(model, session, filters={"id": id_document})
    except HTTPException as e:
        if e.status_code != 404:
            raise
        raise HTTPException(
            status_code=404,
            detail=(
                f"Target document not found: type={document_type.name}({int(document_type)}), id={id_document}"
            ),
        ) from e


def _model_for_document_type(document_type: Any) -> type[SQLModel] | None:
    """Map DocumentTypeEnum to its SQLModel class."""

    from models.constants.types import DocumentTypeEnum

    if document_type == DocumentTypeEnum.FIDELE:
        from models.fidele import Fidele

        return Fidele

    if document_type == DocumentTypeEnum.PAROISSE:
        from models.paroisse import Paroisse

        return Paroisse

    if document_type == DocumentTypeEnum.STRUCTURE:
        from models.constants import Structure

        return Structure

    if document_type == DocumentTypeEnum.NATION:
        from models.adresse import Nation

        return Nation

    if document_type == DocumentTypeEnum.CONTINENT:
        from models.adresse import Continent

        return Continent

    return None


def _document_to_projection(document_type: Any, data: SQLModel) -> BaseModel:
    """Convert a resolved document entity to its projection model.

    This matches your preference: if the document is a paroisse, return a Paroisse projection;
    if it's a fidèle, return a Fidele projection; etc.
    """

    from models.constants.types import DocumentTypeEnum

    if document_type == DocumentTypeEnum.PAROISSE:
        from models.paroisse.projection import ParoisseProjFlat

        return ParoisseProjFlat.model_validate(data)

    if document_type == DocumentTypeEnum.NATION:
        from models.adresse.projection import NationProjFlat

        return NationProjFlat.model_validate(data)

    if document_type == DocumentTypeEnum.CONTINENT:
        from models.adresse.projection import ContinentProjFlat

        return ContinentProjFlat.model_validate(data)

    if document_type == DocumentTypeEnum.STRUCTURE:
        from models.constants.projections import StructureProjFlat

        return StructureProjFlat.model_validate(data)

    if document_type == DocumentTypeEnum.FIDELE:
        from models.fidele.projection import FideleProjFlat

        return FideleProjFlat.model_validate(data)

    # Fallback: expose at least the ID if a new type is added but projections aren't wired yet.
    class _FallbackDoc(BaseModel):
        id: int | None = None

    return _FallbackDoc.model_validate({"id": getattr(data, "id", None)})


async def resolve_document_reference(
    session: AsyncSession,
    *,
    id_document_type: Any,
    id_document: int,
) -> BaseModel | None:
    """Resolve a polymorphic (id_document_type, id_document) reference.

    Returns a small generic dict with the resolved entity fields, or None if unsupported/not found.
    """

    document_type = _coerce_document_type(id_document_type)
    if document_type is None:
        return None

    model = _model_for_document_type(document_type)
    if model is None:
        return None

    from sqlmodel import select

    statement = select(model).where(getattr(model, "id") == id_document)
    if hasattr(model, "est_supprimee"):
        statement = statement.where(getattr(model, "est_supprimee") == False)

    result = await session.exec(statement)
    data = result.first()
    if not data:
        return None

    return _document_to_projection(document_type, data)


async def resolve_document_references_batch(
    session: AsyncSession,
    refs: Iterable[tuple[Any, int]],
) -> dict[tuple[int, int], BaseModel]:
    """Batch-resolve polymorphic document references.

    This avoids the N+1 query problem by doing:
    - 1 query per document type present in the input refs

    Returns a mapping: (id_document_type, id_document) -> resolved payload.
    """

    from sqlmodel import select

    ids_by_type: dict[Any, set[int]] = {}
    for raw_document_type, id_document in refs:
        document_type = _coerce_document_type(raw_document_type)
        if document_type is None:
            continue
        ids_by_type.setdefault(document_type, set()).add(int(id_document))

    resolved: dict[tuple[int, int], BaseModel] = {}
    for document_type, ids in ids_by_type.items():
        model = _model_for_document_type(document_type)
        if model is None:
            continue

        statement = select(model).where(getattr(model, "id").in_(ids))
        if hasattr(model, "est_supprimee"):
            statement = statement.where(getattr(model, "est_supprimee") == False)

        result = await session.exec(statement)
        for data in result.all():
            key = (int(document_type), int(getattr(data, "id")))
            resolved[key] = _document_to_projection(document_type, data)

    return resolved
