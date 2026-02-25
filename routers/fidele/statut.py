from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.adresse import Adresse, Nation
from models.constants import DocumentStatut
from models.constants.types import DocumentTypeEnum, FideleTypeEnum
from models.fidele import (
    Fidele,
    FideleParoisse,
)
from models.fidele.projection import FideleProjFlat, FideleProjShallow
from models.fidele.utils import FideleStatutUpdate
from routers.dependencies import check_resource_exists
from routers.fidele.utils import required_fidele, get_fidele_complete_data_by_id
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send400
from routers.fidele.docs import FIDELE_STATUT_UPDATE_DESCRIPTION
from utils.constants import ProjDepth


fidele_statut_router = APIRouter(prefix="/{id}/statut", tags=["Fidele - Statut"])


PENDING_STATUT_ID = 1
VALIDATED_STATUT_ID = 29


def build_fidele_code(iso_alpha_2: str, fidele_id: int) -> str:
    return f"{iso_alpha_2.upper()}{str(fidele_id).zfill(8)}"


async def get_fidele_paroisse_nation_iso_alpha_2(
    fidele_id: int,
    session: AsyncSession,
) -> str | None:
    membership_stmt = (
        select(FideleParoisse)
        .where(
            (FideleParoisse.id_fidele == fidele_id)
            & (FideleParoisse.est_supprimee == False)
            & (FideleParoisse.est_actif == True)
        )
        .order_by(FideleParoisse.id.desc())
    )
    membership_result = await session.exec(membership_stmt)
    membership = membership_result.first()
    if not membership:
        return None

    adresse_stmt = (
        select(Adresse)
        .where(
            (Adresse.id_document_type == DocumentTypeEnum.PAROISSE.value)
            & (Adresse.id_document == membership.id_paroisse)
            & (Adresse.est_supprimee == False)
        )
        .options(selectinload(Adresse.nation))
    )
    adresse_result = await session.exec(adresse_stmt)
    paroisse_adresse = adresse_result.first()
    if not paroisse_adresse or not paroisse_adresse.nation:
        return None

    return paroisse_adresse.nation.iso_alpha_2


@fidele_statut_router.put("", description=FIDELE_STATUT_UPDATE_DESCRIPTION)
async def update_fidele_statut(
    body: FideleStatutUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleProjFlat | FideleProjShallow:
    """
    Mettre à jour le statut d'un fidèle.

    Règles métier:
    - le code_matriculation est attribué uniquement lors du passage `En attente (1)` -> `Validé (29)`
    - les sympathisants (`id_fidele_type=2`) ne reçoivent pas de code
    - `id_fidele_recenseur` est requis lors de la validation
    """

    await check_resource_exists(DocumentStatut, session, filters={"id": body.id_document_statut})

    current_statut_id = fidele.id_document_statut
    target_statut_id = body.id_document_statut
    is_transition_pending_to_validated = (
        current_statut_id == PENDING_STATUT_ID and target_statut_id == VALIDATED_STATUT_ID
    )

    if is_transition_pending_to_validated and body.id_fidele_recenseur is None:
        return send400(["body", "id_fidele_recenseur"], "Le recenseur est requis lors de la validation")

    if body.id_fidele_recenseur is not None:
        await check_resource_exists(Fidele, session, filters={"id": body.id_fidele_recenseur})

    fidele.id_document_statut = target_statut_id

    if is_transition_pending_to_validated:
        fidele.id_fidele_recenseur = body.id_fidele_recenseur

        if fidele.id_fidele_type != FideleTypeEnum.SYMPATHISANT.value:
            iso_alpha_2 = await get_fidele_paroisse_nation_iso_alpha_2(fidele.id, session)
            if not iso_alpha_2:
                return send400(
                    ["body", "id_document_statut"],
                    "Impossible de générer le code: nation de la paroisse active introuvable",
                )
            fidele.code_matriculation = build_fidele_code(iso_alpha_2, fidele.id)

    fidele.date_modification = datetime.now(timezone.utc)

    session.add(fidele)
    await session.commit()

    if proj == ProjDepth.SHALLOW:
        fidele = await get_fidele_complete_data_by_id(fidele.id, session, proj)

    projected_response = apply_projection(fidele, FideleProjFlat, FideleProjShallow, proj)
    return send200(projected_response)
