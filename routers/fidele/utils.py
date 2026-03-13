import unicodedata
from datetime import date
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from models.adresse import Adresse, Nation
from models.fidele import (
    Fidele,
    FideleStructure,
    FideleParoisse,
    FideleBapteme,
    FideleOrigine,
    FideleOccupation,
)
from fastapi import Depends, Path
from routers.utils import check_resource_exists
from core.db import get_session
from utils.constants import ProjDepth


FIDELE_ALLOWED_INCLUDES = {"photo_url"}


def parse_fidele_include(include: str | None) -> set[str]:
    if not include:
        return set()

    include_fields = {
        item.strip().lower()
        for item in include.split(",")
        if item and item.strip()
    }

    # backward compatibility: include=photo behaves like include=photo_url
    if "photo" in include_fields:
        include_fields.add("photo_url")

    return include_fields.intersection(FIDELE_ALLOWED_INCLUDES)


async def required_fidele(
    id: Annotated[int, Path(..., description="Fidele's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Fidele:
    print(f"Checking existence of fidele with id:::::::------- {id}")
    return await check_resource_exists(Fidele, session, filters={"id": id})


async def get_fidele_complete_data_by_id(
    id: int,
    session: AsyncSession,
    proj: ProjDepth = ProjDepth.SHALLOW,
    include_fields: set[str] | None = None,
) -> Fidele:
    include_fields = include_fields or set()

    statement = select(Fidele).where(Fidele.id == id)
    if proj == ProjDepth.SHALLOW:
        statement = statement.options(
            selectinload(Fidele.grade),
            selectinload(Fidele.fidele_type),
            selectinload(Fidele.fidele_recenseur),
            selectinload(Fidele.nation_nationalite),
            selectinload(Fidele.document_statut),
            selectinload(Fidele.contact),
            selectinload(Fidele.adresse).selectinload(Adresse.nation).selectinload(Nation.continent),
            selectinload(Fidele.photo),
            selectinload(Fidele.structures).selectinload(FideleStructure.structure),
            selectinload(Fidele.paroisses).selectinload(FideleParoisse.paroisse),
            selectinload(Fidele.bapteme).selectinload(FideleBapteme.paroisse),
            selectinload(Fidele.famille),
            selectinload(Fidele.origine).selectinload(FideleOrigine.nation),
            selectinload(Fidele.occupation).selectinload(FideleOccupation.niveau_etude),
            selectinload(Fidele.occupation).selectinload(FideleOccupation.profession),
        )
    elif "photo_url" in include_fields:
        statement = statement.options(selectinload(Fidele.photo))

    result = await session.exec(statement)
    return result.first()


def flatten_letters(value: str) -> str:
    """Normalize and keep only ASCII letters in upper-case."""
    normalized = unicodedata.normalize("NFD", value or "")
    without_diacritics = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return "".join(ch for ch in without_diacritics.upper() if "A" <= ch <= "Z")


def extract_two_letters_prefer_consonants(value: str) -> str:
    """Extract two letters, preferring consonants and falling back to vowels."""
    letters = flatten_letters(value)
    vowels = {"A", "E", "I", "O", "U", "Y"}
    consonants = [ch for ch in letters if ch not in vowels]

    selected = consonants[:2]
    if len(selected) < 2:
        for ch in letters:
            if ch not in selected:
                selected.append(ch)
            if len(selected) == 2:
                break

    while len(selected) < 2:
        selected.append("X")

    return "".join(selected)


async def _get_next_matricule_suffix_letter(
    session: AsyncSession,
    *,
    prefix: str,
) -> str:
    """Return the next suffix letter (A..Z) for a given matricule prefix."""
    stmt = select(Fidele.code_matriculation).where(
        (Fidele.code_matriculation.is_not(None))
        & (Fidele.code_matriculation.like(f"{prefix}%"))
    )
    result = await session.exec(stmt)
    existing_codes = [code for code in result.all() if code]

    max_ord = 64
    for code in existing_codes:
        if len(code) != 12 or not code.startswith(prefix):
            continue
        suffix = code[-1]
        if "A" <= suffix <= "Z":
            max_ord = max(max_ord, ord(suffix))

    if max_ord >= ord("Z"):
        return "Z"
    return chr(max_ord + 1)


async def build_fidele_matricule(
    session: AsyncSession,
    *,
    iso_alpha_2: str,
    id_structure_principale: int,
    nom: str,
    prenom: str,
    date_naissance: date,
) -> str:
    """
    Build a fidele matricule with this structure:
    - 2 letters country ISO code
    - 3 digits principal structure id
    - 2 letters from nom (prefer consonants)
    - 2 letters from prenom (prefer consonants)
    - 2 digits birth year
    - 1 uniqueness suffix letter (A..Z)
    """
    iso = flatten_letters(iso_alpha_2)[:2].ljust(2, "X")
    structure_part = str(int(id_structure_principale)).zfill(3)
    nom_part = extract_two_letters_prefer_consonants(nom)
    prenom_part = extract_two_letters_prefer_consonants(prenom)
    year_part = str(date_naissance.year)[-2:]

    prefix = f"{iso}{structure_part}{nom_part}{prenom_part}{year_part}"
    suffix = await _get_next_matricule_suffix_letter(session, prefix=prefix)
    return f"{prefix}{suffix}"
