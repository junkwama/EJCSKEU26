# External modules
from enum import Enum
from pydantic import ValidationError
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, TypedDict

# Local modules
from utils.utils import log

# Custom HTTP codes
HTTPCodeEntry = TypedDict("HTTPCodeEntry", {"code": int, "message": str})


HTTP_CODES: dict[int, HTTPCodeEntry] = {
    200: {
        "code": status.HTTP_200_OK,
        "message": "Ok"
    },
    400: {
        "code": status.HTTP_400_BAD_REQUEST,
        "message": "Bad Request: The server could not understand the request due to invalid syntax."
    },
    401: {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "Unauthorized: The client must authenticate itself to get the requested response."
    },
    403: {
        "code": status.HTTP_403_FORBIDDEN,
        "message": "Forbidden: The client does not have access rights to the content."
    },
    404: {
        "code": status.HTTP_404_NOT_FOUND,
        "message": "Not Found: The server can not find the requested resource."
    },
    409: {
        "code": status.HTTP_409_CONFLICT,
        "message": "Conflict: The request conflicts with the current state of the server."
    },
    422: {
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": "Unprocessable Entity: The server understands the content type of the request entity, but was unable to process the contained instructions because one of its items is invalid"
    },
    500: {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Internal Server Error: The server has encountered a situation it doesn't know how to handle."
    }
}


# Custom error types
class ErrorTypes(Enum):
    value_error = "Invalid value provided"
    type_error = "Type mismatch error"
    missing_error = "Required field is missing"
    not_found_error = "Resource not found"
    validation_error = "Validation failed"
    permission_error = "Permission denied"
    database_error = "Database access error"
    timeout_error = "Request timeout"
    authentication_error = "Authentication failed"
    authorization_error = "Authorization failed"

# def get_error_details(
#     type: str | None = None, loc: list | None = None,
#     msg: str | None = None, input: Any | None = None
# ) -> dict: return {"type": type, "loc": loc, "msg": msg, "input": input}


def send(
    data: object | None = None,
    error_message: str | None = None,
    code: int | None = HTTP_CODES[200]["code"],
    error_location: str | None = None,
    error_field: str | None = None,
    error_type: str | None = None,
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


def send401(error_message: str | None = None):
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


def send409(error_location: list, error_message: str | None = None):
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

