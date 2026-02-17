from __future__ import annotations

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.constants.types import DocumentTypeEnum
from models.fidele import Fidele
from modules.file.models import File as FileModel, FileProjFlat
from modules.file import get_s3_service, S3Service
from core.db import get_session
from modules.file.utils import get_upload_file_extension
from routers.fidele.utils import required_fidele
from routers.utils.http_utils import send200

fidele_photo_router = APIRouter(prefix="/{id}/photo", tags=["Fidele - photo"])

def fidele_photo_base_key(fidele_id: int) -> str:
    return f"fidele/{fidele_id}/fidele_{fidele_id}_photo"


async def hard_delete_previous_fidele_photos(
    session: AsyncSession,
    file_service: S3Service,
    fidele_id: int,
    keep_key: str,
) -> None:
    photo_base_key = fidele_photo_base_key(fidele_id)
    statement = select(FileModel).where(
        (FileModel.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (FileModel.id_document == fidele_id)
        & (FileModel.est_supprimee == False)
    )
    result = await session.exec(statement)
    files = result.all()

    for db_file in files:
        is_fidele_photo = db_file.file_name.startswith(f"{photo_base_key}.")
        if not is_fidele_photo or db_file.file_name == keep_key:
            continue
        await file_service.delete_file(session, db_file.file_name)


@fidele_photo_router.post("")
async def upload_file(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
    file: S3Service = Depends(get_s3_service),
) -> FileProjFlat:

    extension = get_upload_file_extension(file.file)
    if not extension:
        raise HTTPException(400, "Impossible de déterminer l'extension du fichier")

    photo_key = fidele_photo_base_key(fidele.id) + f".{extension}"

    await hard_delete_previous_fidele_photos(
        session=session,
        file_service=file,
        fidele_id=fidele.id,
        keep_key=photo_key,
    )

    db_file = await file.upload_file(
        session=session,
        s3_key=photo_key,
        id_document_type=DocumentTypeEnum.FIDELE.value,
        id_document=fidele.id,
        allowed_extensions=["jpg", "jpeg", "png"],
        original_name=file.file.filename,
    )

    return send200(db_file)


@fidele_photo_router.get("")
async def get_photo(
    session: Annotated[AsyncSession, Depends(get_session)],
    fidele: Annotated[Fidele, Depends(required_fidele)],
) -> FileProjFlat:
    statement = select(FileModel).where(
        (FileModel.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (FileModel.id_document == fidele.id)
        & (FileModel.est_supprimee == False)
    )
    result = await session.exec(statement)
    db_file = result.first()

    return send200(db_file)