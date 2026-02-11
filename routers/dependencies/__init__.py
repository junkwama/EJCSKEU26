from typing import Any, Mapping, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import and_
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T", bound=SQLModel)


async def check_resource_exists(
    model: Type[T],
    session: AsyncSession,
    *,
    filters: Mapping[str, Any] | None = None,
) -> T:
    """
    Generic dependency to check if a resource exists using MANY columns.

    Args:
        model: SQLModel class to query
        session: Database session
        filters: mapping of model field names to values (combined with AND)

    Example:
        await check_resource_exists(
            Direction,
            session,
            filters={"id_structure": 1, "id_document_type": 5, "id_document": 10},
        )
    """
    if not filters:
        raise ValueError("check_resource_exists requires at least one filter")

    clauses = []
    for field_name, value in filters.items():
        if not hasattr(model, field_name):
            raise ValueError(f"{model.__name__} has no field '{field_name}'")
        clauses.append(getattr(model, field_name) == value)

    # soft-delete filter (if model has est_supprimee)
    if hasattr(model, "est_supprimee"):
        clauses.append(getattr(model, "est_supprimee") == False)

    statement = select(model).where(and_(*clauses))
    result = await session.exec(statement)
    resource = result.first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} not found for filters={dict(filters)}",
        )

    return resource