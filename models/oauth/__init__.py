import re
from pydantic import BaseModel, Field, field_validator

# Local modules
from models.utils.utils import PSW_FIELD_PROPS, Password
from modules.oauth2.models import TokenPayloadBase
from utils.constants import Regex

# Token does not have permission first. 'cause token is stateless 
# We'll be setting it after in CurrentUser

class TokenPayload(TokenPayloadBase):
    """This is the content of the token's payload. It extends the generic TokenPayloadBase with our custom fields."""
    pass

class OauthModel(BaseModel):
    username: str = Field(
        ...,
        examples=["+243814606723"],
        description="Phone number",
    )
    password: Password = Field(..., **PSW_FIELD_PROPS)

    @field_validator("username")
    @classmethod
    def check_oauth_username(cls, value):
        if (
            not re.fullmatch(Regex.PHONE.value, value)
            # and not re.fullmatch(Regex.EMAIL.value, value)
        ):
            raise ValueError(
                "Username must be a valid phone number." # or a valid email address.
            )
        return value
