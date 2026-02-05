from typing import Annotated, Literal
from pydantic import BaseModel

class _ConfigClass(BaseModel):
    TOKEN_EXPIRATION_DAYS: Annotated[int, 1, 365] = 7
    TOKEN_ALGORITHM: Literal["HS256", "RS256"] = "HS256"

    # Default value for the token key. This should be customized with a value from the environment
    BIBIANE_TOKEN_KEY: str = "o?Bx?qE~P\"^69pT" 

# Customize your config values here
Config = _ConfigClass()