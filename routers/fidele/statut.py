from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.adresse import Adresse
from models.constants.types import (
    DocumentStatutEnum,
    DocumentTypeEnum,
    FideleTypeEnum,
    FonctionEnum,
    StructureEnum
)
from models.oauth import TokenPayload
from models.fidele import (
    Fidele,
    FideleParoisse,
)
from models.fidele.projection import FideleProjFlat, FideleProjShallow
from models.fidele.utils import FideleStatutUpdate
from modules.oauth2.dependencies import get_required_token_payload_dependency
from routers.utils import check_resource_exists
from routers.fidele.utils import required_fidele, get_fidele_complete_data_by_id
from routers.utils import apply_projection
from routers.utils.http_utils import send200, send400
from routers.fidele.docs import FIDELE_STATUT_UPDATE_DESCRIPTION
from routers.utils.permissions import require_fidele_direction_fonction 
from utils.constants import ProjDepth

fidele_statut_router = APIRouter(prefix="/{id}/statut", tags=["Fidele - Statut"])

def build_fidele_code(iso_alpha_2: str, fidele_id: int) -> str:
    return f"{iso_alpha_2.upper()}{str(fidele_id).zfill(8)}"

async def get_fidele_paroisse_nation_iso_alpha_2(
    session: AsyncSession,
    fidele_paroisse: FideleParoisse,
) -> str | None:
    
    adresse_stmt = (
        select(Adresse)
        .where(
            (Adresse.id_document_type == DocumentTypeEnum.PAROISSE.value)
            & (Adresse.id_document == fidele_paroisse.id_paroisse)
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
    current_fidele: Annotated[
        TokenPayload,
        Depends(get_required_token_payload_dependency(TokenPayload)),
    ],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    proj: Annotated[ProjDepth, Query()] = ProjDepth.SHALLOW,
) -> FideleProjFlat | FideleProjShallow:
    """
    Mettre à jour le statut d'un fidèle.
    En particulier, cette opération permet de valider un fidèle en attente apres avoir complété le recensement.

    Règles métier:
    - Le code_matriculation est attribué uniquement lors du passage `En attente (1)` -> `Validé (2)`
    - Les sympathisants (`id_fidele_type=2`) ne reçoivent pas de code
    - `id_fidele_recenseur` est requis lors de la validation

    Qui peut faire cette opération ?
    - Les Lesponsables (président), secrétaires et secrétaires adjoints de la paroisse du fidèle peuvent faire cette opération. 
    - Les responsables (présidents), secrétaires et secrétaires adjoints des échelons supérieurs de la paroisse du fidèle (nation, continent, générale).
    Ex: Si le fidèle est dans une paroisse de Paris en France, alors les responsables (présidents), secrétaires et secrétaires adjoints de la paroisse, de la nation (France), du continent (Europe) et de la générale (Nkamba) peuvent faire cette opération.
    """

    current_fidele_statut_id = fidele.id_document_statut
    target_fidele_statut_id = body.id_document_statut
    is_transition_pending_to_validated = (
        current_fidele_statut_id == DocumentStatutEnum.ATTENTE.value and 
        target_fidele_statut_id == DocumentStatutEnum.VALIDE.value
    )

    # 0. A fidele is validated (recensé) only once, when it's done for the first time.
    # So, if the fidele already has a id_fidele_recenseur, it means it's already been validated. 
    # In that case, we silently update the state without affecting the code_matricule nor the id_fidele_recenseur.

    if not fidele.id_fidele_recenseur and is_transition_pending_to_validated:

        # 1: Let's make sure the fidèle currently belongs to a paroisse (active and not deleted), otherwise we won't be able to check permissions nor assign a code matricule if needed
        fidele_paroisse = None
        try:
            fidele_paroisse = await check_resource_exists(
                FideleParoisse,
                session,
                filters={"id_fidele": fidele.id, "est_actif": True, "est_supprimee": False},
            )
        except HTTPException:
            pass
        
        if not fidele_paroisse:
            return send400(
                ["fidele", "id_document_statut"],
                "Le fidèle doit appartenir à une paroisse active pour que son statut puisse être mis à jour.",
            )

        # 2: Let's make sure fidele perfoming the operation has the right permissions (is responsable/president, secrétaire or secrétaire adjoint of the "Bureau Ecclaisiastique" of the "paroisse" or one of its superior echelons)
        await require_fidele_direction_fonction(
            session,
            id_fidele=current_fidele.id,
            id_structure=StructureEnum.BUREAU_ECCLESIASTIQUE,
            functions_set={
                FonctionEnum.RESPONSABLE_PRESIDENT, 
                FonctionEnum.SECRETAIRE, 
                FonctionEnum.SECRETAIRE_ADJOINT
            },
            id_document_type=DocumentTypeEnum.PAROISSE,
            id_document=fidele_paroisse.id_paroisse
        )

        # 3: Assign the logged fidele as recenseur 
        fidele.id_fidele_recenseur = int(current_fidele.sub)

        # 4: Assign a code matricule if the fidèle is a pratiquant (id_fidele_type=1).
        if fidele.id_fidele_type == FideleTypeEnum.PRATIQUANT.value:
            paroisse_nation_iso_alpha_2 = await get_fidele_paroisse_nation_iso_alpha_2(session, fidele_paroisse)
            if not paroisse_nation_iso_alpha_2:
                return send400(
                    ["body", "id_document_statut"],
                    "Impossible de générer le code: nation de la paroisse active introuvable",
                )
            fidele.code_matriculation = build_fidele_code(paroisse_nation_iso_alpha_2, fidele.id)


    # 5: Update the fidèle's statut
    fidele.id_document_statut = target_fidele_statut_id
    fidele.date_modification = datetime.now(timezone.utc)

    session.add(fidele)
    await session.commit()

    if proj == ProjDepth.SHALLOW:
        fidele = await get_fidele_complete_data_by_id(fidele.id, session, proj)

    projected_response = apply_projection(fidele, FideleProjFlat, FideleProjShallow, proj)
    return send200(projected_response)
