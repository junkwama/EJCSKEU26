from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def _has_active_direction_mandate(
    session: AsyncSession,
    *,
    id_direction: int,
    id_fidele: int,
    id_fonction: int,
) -> bool:
    """Return True if fidele holds an active, non-suspended mandate in a direction."""
    from models.direction.fonction import DirectionFonction

    statement = select(DirectionFonction.id).where(
        (DirectionFonction.id_direction == id_direction)
        & (DirectionFonction.id_fidele == id_fidele)
        & (DirectionFonction.id_fonction == id_fonction)
        & (DirectionFonction.est_supprimee == False)
        & (DirectionFonction.est_actif == True)
        & (DirectionFonction.est_suspendu == False)
    )
    result = await session.exec(statement)
    return result.first() is not None


async def _resolve_direction_for_permission_check(
    session: AsyncSession,
    *,
    id_direction: int | None = None,
    id_structure: int | None = None,
    id_document_type: int | None = None,
    id_document: int | None = None,
):
    """
    Resolve a direction either directly by id_direction or by scope tuple
    (id_structure, id_document_type, id_document).
    """
    from models.direction import Direction

    if id_direction is not None:
        statement = select(Direction).where(
            (Direction.id == id_direction) & (Direction.est_supprimee == False)
        )
        return (await session.exec(statement)).first()

    if None in (id_structure, id_document_type, id_document):
        return None

    statement = select(Direction).where(
        (Direction.id_structure == id_structure)
        & (Direction.id_document_type == id_document_type)
        & (Direction.id_document == id_document)
        & (Direction.est_supprimee == False)
    )
    return (await session.exec(statement)).first()


async def _get_superior_scopes_for_direction(
    session: AsyncSession,
    *,
    id_document_type: int,
    id_document: int,
) -> list[tuple[int, int | None]]:
    """
    Resolve supported superior echellons for a direction scope.

    Supported upward traversal for now:
    - PAROISSE -> NATION -> CONTINENT -> GENERALE
    - NATION -> CONTINENT -> GENERALE
    - CONTINENT -> GENERALE
    """
    from models.constants.types import DocumentTypeEnum
    from models.adresse import Adresse, Nation

    if id_document_type == DocumentTypeEnum.PAROISSE.value:
        adresse_stmt = select(Adresse).where(
            (Adresse.id_document_type == DocumentTypeEnum.PAROISSE.value)
            & (Adresse.id_document == id_document)
            & (Adresse.est_supprimee == False)
        )
        adresse = (await session.exec(adresse_stmt)).first()
        if not adresse:
            return []

        nation_stmt = select(Nation).where(Nation.id == adresse.id_nation)
        nation = (await session.exec(nation_stmt)).first()
        if not nation:
            return []

        return [
            (DocumentTypeEnum.NATION.value, nation.id),
            (DocumentTypeEnum.CONTINENT.value, nation.id_continent),
            (DocumentTypeEnum.GENERALE.value, None),
        ]

    if id_document_type == DocumentTypeEnum.NATION.value:
        nation_stmt = select(Nation).where(Nation.id == id_document)
        nation = (await session.exec(nation_stmt)).first()
        if not nation:
            return []

        return [
            (DocumentTypeEnum.CONTINENT.value, nation.id_continent),
            (DocumentTypeEnum.GENERALE.value, None),
        ]

    if id_document_type == DocumentTypeEnum.CONTINENT.value:
        return [(DocumentTypeEnum.GENERALE.value, None)]

    return []


async def has_fidele_direction_fonction(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_fonction: int,
    id_direction: int | None = None,
    id_structure: int | None = None,
    id_document_type: int | None = None,
    id_document: int | None = None,
    include_superior_echellons: bool = True,
) -> bool:
    """
    Check if a fidele has a specific function in a direction.

    When include_superior_echellons=True, also checks superior echellons
    while keeping the same structure (id_structure).
    """
    from models.direction import Direction

    direction = await _resolve_direction_for_permission_check(
        session,
        id_direction=id_direction,
        id_structure=id_structure,
        id_document_type=id_document_type,
        id_document=id_document,
    )
    if not direction:
        return False

    if await _has_active_direction_mandate(
        session,
        id_direction=direction.id,
        id_fidele=id_fidele,
        id_fonction=id_fonction,
    ):
        return True

    if not include_superior_echellons:
        return False

    superior_scopes = await _get_superior_scopes_for_direction(
        session,
        id_document_type=direction.id_document_type,
        id_document=direction.id_document,
    )
    if not superior_scopes:
        return False

    for superior_type, superior_doc_id in superior_scopes:
        direction_stmt = select(Direction.id).where(
            (Direction.est_supprimee == False)
            & (Direction.id_structure == direction.id_structure)
            & (Direction.id_document_type == superior_type)
        )
        if superior_doc_id is not None:
            direction_stmt = direction_stmt.where(Direction.id_document == superior_doc_id)

        direction_ids = (await session.exec(direction_stmt)).all()
        if not direction_ids:
            continue

        for superior_direction_id in direction_ids:
            if await _has_active_direction_mandate(
                session,
                id_direction=superior_direction_id,
                id_fidele=id_fidele,
                id_fonction=id_fonction,
            ):
                return True

    return False


async def require_fidele_direction_fonction(
    session: AsyncSession,
    *,
    id_fidele: int,
    id_fonction: int,
    id_direction: int | None = None,
    id_structure: int | None = None,
    id_document_type: int | None = None,
    id_document: int | None = None,
    include_superior_echellons: bool = True,
) -> None:
    """Raise 403 if fidele does not have required function in direction scope."""
    has_permission = await has_fidele_direction_fonction(
        session,
        id_fidele=id_fidele,
        id_fonction=id_fonction,
        id_direction=id_direction,
        id_structure=id_structure,
        id_document_type=id_document_type,
        id_document=id_document,
        include_superior_echellons=include_superior_echellons,
    )

    if not has_permission:
        raise HTTPException(
            status_code=403,
            detail=(
                "Permission refusée: le fidele n'occupe pas cette fonction "
                "dans la direction cible ni dans les echelons superieurs autorises."
            ),
        )
