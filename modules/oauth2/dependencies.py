from typing import Annotated, Callable, Type, TypeVar
from fastapi import Depends, HTTPException

from .utils import secury_scheme, OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS
from .models import AccessToken, TokenPayloadBase

CustomizedGenericTokenPayload = TypeVar(
    "CustomizedGenericTokenPayload", bound=TokenPayloadBase
)

def get_token_payload_dependency(
    TokenPayloadClass: Type[CustomizedGenericTokenPayload],
    token_required: bool = False
) -> Callable[..., CustomizedGenericTokenPayload | None]:
    """
    Returns a dependency function that extracts the token from the request and verifies it.
    The returned function returns:
        * The token payload of the provided TokenPayloadClass type.
        * None if the token is invalid or does NOT exists.
    """
    def get_token_payload(
        token: str = Depends(secury_scheme),
    ) -> CustomizedGenericTokenPayload | None:

        token_payload = AccessToken[TokenPayloadClass].verity(token, TokenPayloadClass, token_required)
        if not token_payload:
            return None
        return TokenPayloadClass(**token_payload.model_dump())

    return get_token_payload


def get_required_token_payload_dependency(
    TokenPayloadClass: Type[CustomizedGenericTokenPayload],
) -> Callable[..., CustomizedGenericTokenPayload]:
    """
    Returns a dependency function that extracts the token from the request and verifies it.
    Note that this function is used when the token is required.
    The returned function returns:
        * The token payload of the provided TokenPayloadClass type.
        * Raises a 401 if the token is invalid, expired or does NOT exists.
    """
    def get_required_token_payload(
        cur_user: Annotated[
            CustomizedGenericTokenPayload,
            Depends(get_token_payload_dependency(TokenPayloadClass, True)),
        ],
    ) -> CustomizedGenericTokenPayload:
        if not cur_user:
            raise HTTPException(OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS)
        return cur_user

    return get_required_token_payload
