import mimetypes
import os

from fastapi import UploadFile

MIME_EXTENSION_FALLBACK = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "text/plain": "txt",
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}


def get_upload_file_extension(file: UploadFile) -> str | None:
    file_name = file.filename or ""
    _, extension = os.path.splitext(file_name)
    if extension:
        return extension.replace(".", "").lower()

    content_type = file.content_type or ""
    if content_type:
        guessed_extension = mimetypes.guess_extension(content_type)
        if guessed_extension:
            return guessed_extension.replace(".", "").lower()
        fallback_extension = MIME_EXTENSION_FALLBACK.get(content_type)
        if fallback_extension:
            return fallback_extension

    return None
