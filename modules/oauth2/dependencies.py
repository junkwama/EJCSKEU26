from typing import Annotated, Callable, Type, TypeVar
from fastapi import Depends, HTTPException, Request

from .utils import secury_scheme, OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS
from .models import AccessToken, TokenPayloadBase

CustomizedGenericTokenPayload = TypeVar(
    "CustomizedGenericTokenPayload", bound=TokenPayloadBase
)

def get_token_payload_dependency(
    TokenPayloadClass: Type[CustomizedGenericTokenPayload],
    token_required: bool = False,
) -> Callable[..., None]:
    def get_token_payload(
        request: Request,
        token: str = Depends(secury_scheme),
    ) -> None:
        
        # 1) Already validated in this request: do not decode again
        if getattr(request.state, "token_validation_done", False):
            if token_required and request.state.current_fidele is None:
                raise HTTPException(OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS)
            return

        # 2) First validation attempt
        payload = AccessToken[TokenPayloadClass].verity(
            token, TokenPayloadClass, False  # do not raise here
        )

        request.state.token_validation_done = True
        request.state.token_present = bool(token)
        request.state.current_fidele = (
            TokenPayloadClass(**payload.model_dump()) if payload else None
        )

        if token_required and request.state.current_fidele is None:
            raise HTTPException(OAUTH_TOKEN_ERROR_CODE, OAUTH_TOKEN_ERROR_MESS)

    return get_token_payload


def get_required_token_payload_dependency(
    TokenPayloadClass: Type[CustomizedGenericTokenPayload],
) -> Callable[..., CustomizedGenericTokenPayload]:
    def get_required_token_payload(
        request: Request,
        _: Annotated[None, Depends(get_token_payload_dependency(TokenPayloadClass, True))],
    ) -> CustomizedGenericTokenPayload:
        return request.state.current_fidele

    return get_required_token_payload
