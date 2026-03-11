from typing import Annotated, Callable, Type, TypeVar
from fastapi import Depends, HTTPException, Request

from .utils import secury_scheme, OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS
from .models import AccessToken, TokenPayloadBase

CustomizedGenericTokenPayload = TypeVar(
    "CustomizedGenericTokenPayload", bound=TokenPayloadBase
)

def get_token_payload_dependency(
    TokenPayloadClass: Type[CustomizedGenericTokenPayload],
    token_required: bool = False
) -> Callable[..., None]:
    """
    Returns a dependency function that extracts the token from the request and verifies it.
    Stores the resolved token payload in request.state.current_fidele.
    """
    def get_token_payload(
        request: Request,
        token: str = Depends(secury_scheme),
    ) -> None:

        token_payload = AccessToken[TokenPayloadClass].verity(token, TokenPayloadClass, token_required)
        request.state.current_fidele = (
            TokenPayloadClass(**token_payload.model_dump()) if token_payload else None
        )

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
        request: Request,
        _: Annotated[
            None,
            Depends(get_token_payload_dependency(TokenPayloadClass, True)),
        ],
    ) -> CustomizedGenericTokenPayload:
        cur_user = getattr(request.state, "current_fidele", None)
        if not cur_user:
            raise HTTPException(OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS)
        return cur_user

    return get_required_token_payload
