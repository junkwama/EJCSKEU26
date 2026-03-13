from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.constants.types import DocumentTypeEnum, FonctionEnum, StructureEnum


def _normalize_functions_set(
    *,
    functions_set: set[FonctionEnum] | None = None,
) -> list[int]:
    """Validate functions_set and convert enum values to integer ids."""
    if not functions_set:
        return []

    normalized: list[int] = []
    for fonction in functions_set:
        if not isinstance(fonction, FonctionEnum):
            raise HTTPException(
                status_code=422,
                detail="functions_set doit contenir uniquement des valeurs FonctionEnum.",
            )

        normalized.append(int(fonction.value))

    return normalized


def _normalize_structure_id(value: StructureEnum | int | None) -> int | None:
    """Normalize structure enum/int to raw integer id for SQL filters."""
    if value is None:
        return None
    if isinstance(value, StructureEnum):
        return int(value.value)
    if isinstance(value, int) and value > 0:
        return value
    raise HTTPException(
        status_code=422,
        detail="id_structure doit etre un StructureEnum valide.",
    )


def _normalize_document_type_id(value: DocumentTypeEnum | int | None) -> int | None:
    """Normalize document type enum/int to raw integer id for SQL filters."""
    if value is None:
        return None
    if isinstance(value, DocumentTypeEnum):
        return int(value.value)
    if isinstance(value, int) and value > 0:
        return value
    raise HTTPException(
        status_code=422,
        detail="id_document_type doit etre un DocumentTypeEnum valide.",
    )


async def _has_active_direction_mandate(
    session: AsyncSession,
    *,
    id_direction: int,
    id_fidele: int,
    id_fonctions: list[int],
) -> bool:
    """Return True if fidele holds at least one active mandate in a direction."""
    from models.direction.fonction import DirectionFonction

    if not id_fonctions:
        return False

    statement = select(DirectionFonction.id).where(
        (DirectionFonction.id_direction == id_direction)
        & (DirectionFonction.id_fidele == id_fidele)
        & (DirectionFonction.id_fonction.in_(id_fonctions))
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
    id_structure: StructureEnum | int | None = None,
    id_document_type: DocumentTypeEnum | int | None = None,
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

    normalized_structure_id = _normalize_structure_id(id_structure)
    normalized_document_type_id = _normalize_document_type_id(id_document_type)

    if None in (normalized_structure_id, normalized_document_type_id, id_document):
        return None

    statement = select(Direction).where(
        (Direction.id_structure == normalized_structure_id)
        & (Direction.id_document_type == normalized_document_type_id)
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
    functions_set: set[FonctionEnum] | None = None,
    id_direction: int | None = None,
    id_structure: StructureEnum | None = None,
    id_document_type: DocumentTypeEnum | None = None,
    id_document: int | None = None,
    include_superior_echellons: bool = True,
) -> bool:
    """
    Check if a fidele has at least one function from functions_set in a direction.

    When include_superior_echellons=True, also checks superior echellons
    while keeping the same structure (id_structure).
    """
    from models.direction import Direction

    fonction_ids = _normalize_functions_set(functions_set=functions_set)
    if not fonction_ids:
        return False

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
        id_fonctions=fonction_ids,
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
                id_fonctions=fonction_ids,
            ):
                return True

    return False


async def require_fidele_direction_fonction(
    session: AsyncSession,
    *,
    id_fidele: int,
    functions_set: set[FonctionEnum] | None = None,
    id_direction: int | None = None,
    id_structure: StructureEnum | None = None,
    id_document_type: DocumentTypeEnum | None = None,
    id_document: int | None = None,
    include_superior_echellons: bool = True,
) -> None:
    """Raise 403 if fidele does not have at least one required function."""
    fonction_ids = _normalize_functions_set(functions_set=functions_set)
    if not fonction_ids:
        raise HTTPException(
            status_code=422,
            detail="functions_set doit contenir au moins une fonction.",
        )

    has_permission = await has_fidele_direction_fonction(
        session,
        id_fidele=id_fidele,
        functions_set=functions_set,
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
                "Permission refusée: le fidele n'occupe aucune des fonctions demandées "
                "dans la direction cible ni dans les echelons superieurs autorises."
            ),
        )
