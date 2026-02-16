from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.db import get_session
from models.constants import DocumentStatut
from models.constants.projections import DocumentStatutProjFlat
from models.constants.utils import DocumentStatutBase, DocumentStatutUpdate
from routers.dependencies import check_resource_exists
from routers.utils.http_utils import send200


document_statut_router = APIRouter(prefix="/document_statut", tags=["Constants - Document Statuts"])


async def required_document_statut(
    id: Annotated[int, Path(..., description="DocumentStatut's ID")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentStatut:
    return await check_resource_exists(DocumentStatut, session, filters={"id": id})


@document_statut_router.get("")
async def get_document_statuts(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[DocumentStatutProjFlat]:
    statement = select(DocumentStatut).where(DocumentStatut.est_supprimee == False)
    result = await session.exec(statement)
    statuts = result.all()
    return send200([DocumentStatutProjFlat.model_validate(s) for s in statuts])


@document_statut_router.post("")
async def create_document_statut(
    body: DocumentStatutBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentStatutProjFlat:
    statut = DocumentStatut.model_validate(body, from_attributes=True)
    session.add(statut)
    await session.commit()
    await session.refresh(statut)

    return send200(DocumentStatutProjFlat.model_validate(statut))


@document_statut_router.put("/{id}")
async def update_document_statut(
    body: DocumentStatutUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    statut: Annotated[DocumentStatut, Depends(required_document_statut)],
) -> DocumentStatutProjFlat:
    update_data = body.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(statut, field, value)

    statut.date_modification = datetime.now(timezone.utc)

    session.add(statut)
    await session.commit()

    return send200(DocumentStatutProjFlat.model_validate(statut))
