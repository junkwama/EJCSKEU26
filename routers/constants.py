from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# Local modules
from core.db import get_session
from models.constants import FideleType, Grade, DocumentType
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
constants_router = APIRouter(tags=["Constants"])


# ============================================================================
# ENDPOINTS
# ============================================================================
@constants_router.get("/types_document")
async def get_document_types(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[DocumentType]:
    """
    Récupérer les types de documents disponibles (FIDELE, PAROISSE, STRUCTURE)

    Returns:
        Liste des types de documents disponibles
    """
    statement = select(DocumentType)
    result = await session.exec(statement)
    document_types = result.all()

    return send200(document_types)


@constants_router.get("/grades")
async def get_grades(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[Grade]:
    """
    Récupérer les grades ecclésiastiques disponibles

    Returns:
        Liste des grades ecclésiastiques
    """
    statement = select(Grade).where(Grade.est_supprimee == False)
    result = await session.exec(statement)
    grades = result.all()

    return send200(grades)


@constants_router.get("/fidele_types")
async def get_fidele_types(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[FideleType]:
    """
    Récupérer les types de fidèles disponibles

    Returns:
        Liste des types de fidèles (Pratiquant, Sympathisant, etc.)
    """
    statement = select(FideleType).where(FideleType.est_supprimee == False)
    result = await session.exec(statement)
    fidele_types = result.all()

    return send200(fidele_types)
