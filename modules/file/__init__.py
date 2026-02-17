import os
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError
from fastapi import File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.file.models import File as FileModel, FileProjFlat
from modules.file.utils import get_upload_file_extension

class S3Service:

    file: UploadFile
    
    def __init__(self, file: UploadFile):
        self.file = file

        # checking if AWS credentials are set
        aws_access_key_id = os.getenv("AWS_S3_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_S3_REGION")
        aws_bucket = os.getenv("AWS_S3_BUCKET")
        if not aws_access_key_id or not aws_secret_access_key or not aws_region or not aws_bucket:
            raise HTTPException(500, "Configuration AWS S3 incomplète")

        try:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region,
            )
        except Exception:
            raise HTTPException(500, "Impossible d'initialiser le client AWS S3")

        self.bucket = aws_bucket

    async def save_metadata_to_db(
        self,
        session: AsyncSession,
        *,
        s3_key: str,
        id_document_type: int,
        id_document: int,
        url_expires_in: int,
        original_name: str | None,
    ) -> FileProjFlat:
        signed_url = self.sign_url(s3_key, url_expires_in)
        signed_url_expiration_date = datetime.now(timezone.utc) + timedelta(seconds=url_expires_in)

        statement = select(FileModel).where(FileModel.file_name == s3_key)
        result = await session.exec(statement)
        db_file = result.first()

        if db_file:
            db_file.original_name = original_name
            db_file.mimetype = self.file.content_type
            db_file.size = self.file.size or 0
            db_file.signed_url = signed_url
            db_file.signed_url_expiration_date = signed_url_expiration_date
            db_file.id_document_type = id_document_type
            db_file.id_document = id_document
            db_file.est_supprimee = False
            db_file.date_suppression = None
            db_file.date_modification = datetime.now(timezone.utc)
        else:
            db_file = FileModel(
                original_name=original_name,
                file_name=s3_key,
                mimetype=self.file.content_type,
                size=self.file.size or 0,
                signed_url=signed_url,
                signed_url_expiration_date=signed_url_expiration_date,
                id_document_type=id_document_type,
                id_document=id_document,
            )
            session.add(db_file)

        await session.commit()
        await session.refresh(db_file)

        return FileProjFlat.model_validate(db_file)

    async def upload_file(
        self,
        session: AsyncSession,
        *,
        s3_key: str,
        id_document_type: int,
        id_document: int,
        allowed_extensions: list[str] | set[str],
        url_expires_in: int = 3600 * 60,
        original_name: str | None = None,
    ) -> FileProjFlat:
        
        if not self.file:
            raise HTTPException(401, "Aucun fichier fourni")
        elif not original_name:
            original_name = self.file.filename

        if not self.file.content_type:
            raise HTTPException(401, "Le type du fichier est requis")

        file_extension = get_upload_file_extension(self.file)
        if not file_extension:
            raise HTTPException(400, "Impossible de déterminer l'extension du fichier")

        normalized_allowed_extensions = {
            extension.strip().lower().lstrip(".") for extension in allowed_extensions if extension
        }
        if not normalized_allowed_extensions:
            raise HTTPException(500, "Aucune extension autorisée configurée")

        if file_extension not in normalized_allowed_extensions:
            raise HTTPException(
                400,
                f"Extension de fichier non autorisée: .{file_extension}",
            )

        try:
            self.client.upload_fileobj(
                self.file.file,
                self.bucket,
                s3_key,
                ExtraArgs={"ContentType": self.file.content_type},
            )

            return await self.save_metadata_to_db(
                session,
                s3_key=s3_key,
                id_document_type=id_document_type,
                id_document=id_document,
                url_expires_in=url_expires_in,
                original_name=original_name,
            )
        except ClientError:
            raise HTTPException(500, "Échec de l'upload du fichier vers S3")
        except IntegrityError:
            await session.rollback()
            raise HTTPException(409, "Conflit sur le nom du fichier")
        except HTTPException:
            raise
        except Exception:
            await session.rollback()
            raise HTTPException(500, "Erreur interne pendant l'upload du fichier")

    def sign_url(self, s3_key: str, expires_in: int = 3600 * 60):
        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": s3_key},
                ExpiresIn=expires_in,
            )
        except Exception:
            raise HTTPException(500, "Erreur interne pendant la génération de l'URL signée")

    async def delete_file(self, session: AsyncSession, s3_key: str) -> FileProjFlat:
        try:
            statement = select(FileModel).where(
                (FileModel.file_name == s3_key) & (FileModel.est_supprimee == False)
            )
            result = await session.exec(statement)
            db_file = result.first()

            if not db_file:
                raise HTTPException(404, "Fichier non trouvé")

            self.client.delete_object(Bucket=self.bucket, Key=s3_key)

            db_file.est_supprimee = True
            db_file.date_suppression = datetime.now(timezone.utc)
            db_file.date_modification = datetime.now(timezone.utc)
            db_file.signed_url = None
            db_file.signed_url_expiration_date = None

            await session.commit()
            await session.refresh(db_file)

            return FileProjFlat.model_validate(db_file)
        except ClientError:
            raise HTTPException(500, "Échec de suppression du fichier sur S3")
        except HTTPException:
            raise
        except Exception:
            await session.rollback()
            raise HTTPException(500, "Erreur interne pendant la suppression du fichier")

# Factory function to get the S3 service instance
def get_s3_service(file: UploadFile = File(...)):
    return S3Service(file)