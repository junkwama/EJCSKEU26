from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.constants import RecensementEtape
from models.constants.projections import RecensementEtapeProjFlat
from routers.utils.http_utils import send200

# ============================================================================
# ROUTER SETUP
# ============================================================================
recensement_etape_router = APIRouter(
    prefix="/recensement_etape",
    tags=["Constants - Recensement Etapes"],
)


# ============================================================================
# ENDPOINTS
# ============================================================================
@recensement_etape_router.get("")
async def get_recensement_etapes(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[RecensementEtapeProjFlat]:
    """
    Récupérer la liste des étapes du processus de recensement d'un fidèle.

    Returns:
        Liste des étapes de recensement dans l'ordre (1→10)
    """
    statement = select(RecensementEtape).order_by(RecensementEtape.id)
    result = await session.exec(statement)
    etapes = result.all()
    return send200([RecensementEtapeProjFlat.model_validate(e) for e in etapes])
