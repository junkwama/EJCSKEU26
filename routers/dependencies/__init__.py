from typing import TYPE_CHECKING, Annotated, Type, TypeVar
from fastapi import Depends, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

# Avoid circular dependency
if TYPE_CHECKING:
    from models.fidele import Fidele

from core.db import get_session

T = TypeVar('T', bound=SQLModel)

async def check_resource_exists(
    model: Type[T],
    resource_id: int,
    session: AsyncSession,
    id_field: str = "id",
) -> T:
    """
    Generic dependency to check if a resource exists in the database
    
    Args:
        model: SQLModel class to query
        resource_id: ID value to check
        session: Database session
        id_field: Field name to match against (default: "id")
    
    Returns:
        Resource object if found
    
    Raises:
        HTTPException 404 if not found (using send404 error format)
    
    Example in route:
        @router.get("/{id}")
        async def get_user(
            user: Annotated["User", Depends(
                lambda id, s=Depends(get_session): check_resource_exists(User, id, s)
            )]
        ):
            return send200(UserProj.model_validate(user))
    """
    statement = select(model).where(getattr(model, id_field) == resource_id)
    result = await session.exec(statement)
    resource = result.first()
    
    if not resource:
        # Raise HTTPException with send404 format as detail
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} with {id_field}={resource_id} not found"
        )
    
    return resource


async def required_fidele(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> "Fidele":
    """Get and validate Fidele exists"""
    from models.fidele import Fidele
    return await check_resource_exists(Fidele, id, session)

