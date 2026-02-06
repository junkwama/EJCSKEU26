# External modules
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

# Local modules
from utils.utils import log
from routers.utils.constants import HTTP_CODES, ErrorTypes

# def get_error_details(
#     type: Optional[str] = None, loc: Optional[list] = None,
#     msg: Optional[str] = None, input: Optional[Any] = None
# ) -> dict: return {"type": type, "loc": loc, "msg": msg, "input": input}


def send(
    data: object | None = None,
    error_message: str | None = None,
    code: int | None = HTTP_CODES[200]["code"],
    error_location: Optional[str] = None,
    error_field: Optional[str] = None,
    error_type: Optional[str] = None,
):
    content = {
        "code": code,
        "data": data,
        "error": (
            {
                "type": error_type,
                "message": error_message,
                "location": error_location,
                "field": error_field,
            }
            if (error_type or error_message or error_field or error_location)
            else None
        ),
    }

    return JSONResponse(jsonable_encoder(content), code)


def send200(data: object):
    return send(data)


def send400(error_location: List[str] | None = None, error_message: str | None = None):
    return send(
        error_message=error_message or HTTP_CODES[400]["message"],
        error_type=ErrorTypes.value_error.name,
        code=HTTP_CODES[400]["code"],
        error_location=error_location,
        error_field=(
            error_location[-1] if error_location and len(error_location) else None
        ),
    )


def send401(error_message: Optional[str] = None):
    return send(
        error_message=error_message or HTTP_CODES[401]["message"],
        error_type=ErrorTypes.authentication_error.name,
        code=HTTP_CODES[401]["code"],
        error_location=["headers", "Authorization"],
        error_field="Authorization",
    )


def send403(error_message: str | None = None):
    """The permission error is always related to the token"""
    return send(
        error_message=error_message or HTTP_CODES[403]["message"],
        error_type=ErrorTypes.permission_error.name,
        code=HTTP_CODES[403]["code"],
        error_location=["headers", "Authorization"],
        error_field="Authorization",
    )


def send404(error_location: list[str], error_message: str | None = None):
    return send(
        error_message=error_message or HTTP_CODES[404]["message"],
        error_type=ErrorTypes.not_found_error.name,
        code=HTTP_CODES[404]["code"],
        error_location=error_location,
        error_field=(
            error_location[-1] if error_location and len(error_location) else None
        ),
    )


def send409(error_location: list, error_message: Optional[str] = None):
    return send(
        error_message=error_message or HTTP_CODES[409]["message"],
        error_type=ErrorTypes.database_error.name,
        code=HTTP_CODES[409]["code"],
        error_location=error_location,
        error_field=(
            error_location[-1] if error_location and len(error_location) else None
        ),
    )


def send422(
    error_location: list | None = None,
    error_message: str | None = None,
    exception: ValueError | ValidationError | None = None,
):
    if exception and not error_location:
        error = exception.errors()[0]
        error_location = error["loc"]
        error_message = error["msg"]
        return send422(error_location, error_message)

    # Set the error_field and handle the case when it's a the index of the item causing the error.
    # when the error happend in an array
    error_field = None
    if error_location and len(error_location):
        for i, loc in enumerate(reversed(error_location)):
            if not isinstance(loc, int):
                error_field = loc
                break
            elif i > 0:
                error_field = error_location[-(i + 1)]
                break

    return send(
        error_message=error_message or HTTP_CODES[422]["message"],
        error_type=ErrorTypes.validation_error.name,
        code=HTTP_CODES[422]["code"],
        error_location=error_location,
        error_field=error_field,
    )


def send500(e: Exception | None = None, error_message: str | None = None):

    if error_message:
        log(Exception(error_message))
    elif e:
        log(e)

    return send(
        error_message=error_message or HTTP_CODES[500]["message"],
        code=HTTP_CODES[500]["code"],
    )

    """
    Valide et retourne le type de document et l'ID
    
    Returns:
        tuple: (id_document_type, id_document, error_message)
        - id_document_type: 1=FIDELE, 2=PAROISSE, 3=STRUCTURE
        - id_document: L'ID du document
        - error_message: Message d'erreur si validation échoue, None sinon
    """
    params = [id_fidele, id_paroisse, id_structure]
    provided_params = sum(1 for p in params if p is not None)
    
    if provided_params == 0:
        return None, None, "Au moins un paramètre (id_fidele, id_paroisse ou id_structure) est requis"
    if provided_params > 1:
        return None, None, "Un seul paramètre parmi (id_fidele, id_paroisse, id_structure) doit être fourni"
    
    if id_fidele is not None:
        return 1, id_fidele, None  # 1 = FIDELE
    elif id_paroisse is not None:
        return 2, id_paroisse, None  # 2 = PAROISSE
    else:
        return 3, id_structure, None  # 3 = STRUCTURE