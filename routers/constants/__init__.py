from fastapi import APIRouter
from routers.constants.document_types import document_types_router
from routers.constants.grades import grades_router
from routers.constants.fidele_types import fidele_types_router
from routers.constants.nations import nations_router
from routers.constants.mouvements_association import mouvements_router
from routers.constants.fonctions import fonctions_router

# ============================================================================
# CONSTANTS ROUTER AGGREGATOR
# ============================================================================
constants_router = APIRouter()

# Include all sub-routers
constants_router.include_router(document_types_router)
constants_router.include_router(grades_router)
constants_router.include_router(fidele_types_router)
constants_router.include_router(nations_router)
constants_router.include_router(mouvements_router)
constants_router.include_router(fonctions_router)
