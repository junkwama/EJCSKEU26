import jwt
from fastapi import HTTPException
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import Type, TypeVar, Generic #, Protocol, runtime_checkable

from .utils import get_token_exp, OAUTH_INVALID_TOKEN_ERROR_MESS, OAUTH_TOKEN_ERROR_CODE
from .config import Config

UserRoleType = TypeVar("UserRoleType", default=str)

class TokenPayloadBase(BaseModel, Generic[UserRoleType]):
    """
    This model defines the content of the token's payload.
    Token should be stateless so can only contain constant data.
    That's why data like permissions are not kept in the token but instead, they are collected when needed
    """

    sub: PydanticObjectId
    exp: int | None = Field(
        default_factory=get_token_exp
    )  # Timestamp int (Without millisecs)
    role: UserRoleType

    # Fields to be added nexts:
    # `expires_in`: The `expires_in` field indicates how long the token is valid for, in seconds. 
    # `scope`: The `scope` field indicates the scope of access that has been granted to the application.
  

    
CustomizedGenericTokenPayload = TypeVar(
    "CustomizedGenericTokenPayload", bound=TokenPayloadBase
)

class AccessToken(BaseModel, Generic[CustomizedGenericTokenPayload]):
    """
    This is the object contained in the token returned after successful oauth and registration

    Dependencies:
        * Requires a child class of TokenPayloadBase as generic type

    Has 2 keys:
        * access_token
        * token_type
    """

    access_token: str # The actual token that is used to authenticate the user. 
    token_type: str | None = Field(default_factory=lambda: "bearer") # The type of token that is being returned, default is "Bearer".  

    @classmethod
    def verity(
        cls,
        token: str,
        TokenPayloadClass: Type[CustomizedGenericTokenPayload],
        token_required: bool = False,
    ) -> CustomizedGenericTokenPayload | None:
        """
        This function verifies the validity of a token.
        Returns:
            * The token payload of type provided as generic type to the class
            * None if token does NOT exists
            * raises a 401 if the token is expired or invalid
        Args:
            * token as The token to verify
            * TokenPayloadClass as The class of the token payload. Must be a child of TokenPayloadBase
            * token_required When True, raises a 401 if the token is invalid or expired
        """

        key = Config.BIBIANE_TOKEN_KEY
        algorithm = Config.TOKEN_ALGORITHM

        if not token:
            return None
        try:
            json_payload = jwt.decode(token, key, algorithms=[algorithm])
            return TokenPayloadClass(**json_payload)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            # If the token is expired or invalid,
            # we return None if token_required is False
            # * and raise an HTTPException if token_required is True
            if token_required:
                raise HTTPException(
                    OAUTH_TOKEN_ERROR_CODE, OAUTH_INVALID_TOKEN_ERROR_MESS
                )
            else:
                return None

# @runtime_checkable
# class OauthModelProtocol(Protocol):
#     # This is the protocole used as interface in python to 
#     # to enforce other class to implement some methods and properties
#     # We use @runtime_checkable decoration to make this checkable 
#     # Since normally Protocol only check at compile time and don't raise runtime errors
#     username: str
#     password: str