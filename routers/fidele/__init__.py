# External moduls
from fastapi import APIRouter, Depends, Path, Query
from typing import Annotated, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

# Local modules
from core.config import Config
from models.fidele import Fidele
from models.fidele.utils import FideleBase
from models.fidele.projection import FideleProjFlat, FideleProjShallow
from core.db import get_session
from routers.utils.http_utils import send200, send404

fidele_router = APIRouter()

@fidele_router.get("")
async def get_fideles(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=Config.MAX_ITEMS_PER_PAGE)] = Config.MAX_ITEMS_PER_PAGE,
) -> List[FideleProjFlat]:
    """
    Recuperer la liste des fideles avec pagination
    """
    # Fetching main data
    statement = select(Fidele).offset(offset).limit(limit)
    
    result = await session.exec(statement)
    fidele_list = result.all()

    # Returning the list
    return send200([
        FideleProjFlat.model_validate(fidele) 
        for fidele in fidele_list
    ])

@fidele_router.get("/{id}")
async def get_fidele(
    id: Annotated[int, Path(..., description="Fidele's Id")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleProjShallow:
    """
    Recuperer un fidele par son Id avec ses relations

    ARGS:
        id (int): L'Id du fidele à récupérer
    """
    # Fetching the requested fidele WITH eager loading
    statement = (
        select(Fidele)
        .where(Fidele.id == id)
        .options(
            selectinload(Fidele.grade),
            selectinload(Fidele.fidele_type),
            selectinload(Fidele.contact),
            selectinload(Fidele.adresse)
        )
    )
    
    result = await session.exec(statement)
    fidele = result.first()


    # If there's no matching fidele
    if not fidele:
        return send404(["body", "id"], "Fidele non existant")

    # Return the fidele as projection
    return send200(FideleProjShallow.model_validate(fidele))

@fidele_router.post("")
async def create_fidele(
    fidele_data: FideleBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FideleProjShallow:
    """
    Créer un nouveau fidele

    ARGS:
        fidele_data (FideleBase): Les données du fidele à créer
    """
    # Create new fidele instance

    new_fidele = Fidele(**fidele_data.model_dump())

    # Add to session and commit
    session.add(new_fidele)
    await session.commit()
    await session.refresh(new_fidele)

    # Return the created fidele
    return send200(FideleProjShallow.model_validate(new_fidele))
