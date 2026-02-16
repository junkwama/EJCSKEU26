from fastapi import APIRouter
from routers.constant.document_type import document_type_router
from routers.constant.document_statut import document_statut_router
from routers.constant.grade import grade_router
from routers.constant.fidele_type import fidele_type_router
from routers.constant.structure_type import structure_type_router
from routers.constant.nation import nation_router
from routers.constant.structure import structure_router
from routers.constant.fonction import fonction_router
from routers.constant.profession import profession_router
from routers.constant.niveau_etudes import niveau_etudes_router
from routers.constant.etat_civile import etat_civile_router

# ============================================================================
# CONSTANTS ROUTER AGGREGATOR
# ============================================================================
constant_router = APIRouter()

# Include all sub-routers
constant_router.include_router(document_type_router)
constant_router.include_router(document_statut_router)
constant_router.include_router(grade_router)
constant_router.include_router(fidele_type_router)
constant_router.include_router(structure_type_router)
constant_router.include_router(nation_router)
constant_router.include_router(structure_router)
constant_router.include_router(fonction_router)
constant_router.include_router(profession_router)
constant_router.include_router(niveau_etudes_router)
constant_router.include_router(etat_civile_router)
