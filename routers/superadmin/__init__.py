from fastapi import APIRouter

from routers.superadmin.fidele import superadmin_fidele_router


superadmin_router = APIRouter()
superadmin_router.include_router(superadmin_fidele_router, prefix="/fidele")
