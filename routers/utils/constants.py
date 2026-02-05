from typing import TypedDict
from fastapi import status
from enum import Enum

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

