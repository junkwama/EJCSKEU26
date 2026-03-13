from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import delete, update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from models.adresse import Adresse
from models.constants.types import DocumentTypeEnum
from models.contact import Contact
from models.direction.fonction import DirectionFonction
from models.fidele import (
    Fidele,
    FideleBapteme,
    FideleFamille,
    FideleOccupation,
    FideleOrigine,
    FideleParoisse,
    FideleRecensementEtape,
    FideleStructure,
)
from modules.file.models import File
from modules.file import get_s3_service_without_file
from routers.utils.http_utils import send200, send404


superadmin_fidele_router = APIRouter(tags=["Superadmin - Fidele"])


@superadmin_fidele_router.delete("/{id_fidele}")
async def hard_delete_fidele(
    id_fidele: Annotated[int, Path(..., description="ID du fidele a supprimer")],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Hard delete complet d'un fidele et de ses donnees rattachees."""
    fidele_stmt = select(Fidele).where(Fidele.id == id_fidele)
    fidele_result = await session.exec(fidele_stmt)
    fidele = fidele_result.first()

    if not fidele:
        return send404(["path", "id_fidele"], "Fidele introuvable")

    now = datetime.now(timezone.utc)

    # Delete photos/files from S3 before hard-deleting their DB metadata.
    file_stmt = select(File).where(
        (File.id_document_type == DocumentTypeEnum.FIDELE.value)
        & (File.id_document == id_fidele)
    )
    file_result = await session.exec(file_stmt)
    fidele_files = file_result.all()

    if fidele_files:
        s3_service = get_s3_service_without_file()
        for db_file in fidele_files:
            if not db_file.file_name:
                continue
            try:
                s3_service.client.delete_object(Bucket=s3_service.bucket, Key=db_file.file_name)
            except Exception:
                raise HTTPException(500, f"Echec de suppression S3 pour le fichier: {db_file.file_name}")

    # Preserve referential integrity for self-references before deleting the fidele.
    await session.exec(
        update(Fidele)
        .where(Fidele.id_fidele_recenseur == id_fidele)
        .values(id_fidele_recenseur=None, date_modification=now)
    )

    # Delete polymorphic resources linked via (id_document_type, id_document).
    await session.exec(
        delete(Contact).where(
            (Contact.id_document_type == DocumentTypeEnum.FIDELE.value)
            & (Contact.id_document == id_fidele)
        )
    )
    await session.exec(
        delete(Adresse).where(
            (Adresse.id_document_type == DocumentTypeEnum.FIDELE.value)
            & (Adresse.id_document == id_fidele)
        )
    )
    await session.exec(
        delete(File).where(
            (File.id_document_type == DocumentTypeEnum.FIDELE.value)
            & (File.id_document == id_fidele)
        )
    )

    # Delete direct relations explicitly for predictable clean-up.
    await session.exec(delete(DirectionFonction).where(DirectionFonction.id_fidele == id_fidele))
    await session.exec(delete(FideleRecensementEtape).where(FideleRecensementEtape.id_fidele == id_fidele))
    await session.exec(delete(FideleStructure).where(FideleStructure.id_fidele == id_fidele))
    await session.exec(delete(FideleParoisse).where(FideleParoisse.id_fidele == id_fidele))
    await session.exec(delete(FideleBapteme).where(FideleBapteme.id_fidele == id_fidele))
    await session.exec(delete(FideleFamille).where(FideleFamille.id_fidele == id_fidele))
    await session.exec(delete(FideleOrigine).where(FideleOrigine.id_fidele == id_fidele))
    await session.exec(delete(FideleOccupation).where(FideleOccupation.id_fidele == id_fidele))

    # Finally delete the fidele row itself.
    await session.exec(delete(Fidele).where(Fidele.id == id_fidele))

    await session.commit()

    return send200({
        "id_fidele": id_fidele,
        "message": "Suppression complete effectuee",
    })
