from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import Grade
from models.constants.utils import GradeBase, GradeUpdate
from models.constants.projections import GradeProjFlat
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
grades_router = APIRouter(prefix="/grades", tags=["Constants - Grades"])


# ============================================================================
# DEPENDENCIES
# ============================================================================
async def required_grade(
    id: Annotated[int, Path(..., description="Grade's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Grade:
    """Get and validate Grade exists"""
    return await check_resource_exists(Grade, id, session)


# ============================================================================
# ENDPOINTS
# ============================================================================
@grades_router.get("")
async def get_grades(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[GradeProjFlat]:
    """
    Récupérer les grades ecclésiastiques disponibles

    Returns:
        Liste des grades ecclésiastiques
    """
    statement = select(Grade).where(Grade.est_supprimee == False)
    result = await session.exec(statement)
    grades = result.all()
    grades_proj = [GradeProjFlat.model_validate(g) for g in grades]

    return send200(grades_proj)


@grades_router.post("")
async def create_grade(
    grade_data: GradeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GradeProjFlat:
    """
    Créer un nouveau grade ecclésiastique

    Args:
        grade_data: Les données du grade à créer

    Returns:
        Le grade créé
    """
    grade = Grade.model_validate(grade_data, from_attributes=True)
    session.add(grade)
    await session.commit()
    await session.refresh(grade)

    return send200(GradeProjFlat.model_validate(grade))


@grades_router.put("/{id}")
async def update_grade(
    grade_data: GradeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    grade: Annotated[Grade, Depends(required_grade)],
) -> GradeProjFlat:
    """
    Mettre à jour un grade ecclésiastique

    Args:
        id: ID du grade à mettre à jour
        grade_data: Les nouvelles données du grade

    Returns:
        Le grade mis à jour
    """
    update_data = grade_data.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(grade, field, value)

    # Update modification timestamp
    grade.date_modification = datetime.now(timezone.utc)

    # Commit changes
    session.add(grade)
    await session.commit()

    projected_response = GradeProjFlat.model_validate(grade)
    return send200(projected_response)