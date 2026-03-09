from typing import Annotated, Literal
from pydantic import BaseModel

class _ConfigClass(BaseModel):
    TOKEN_EXPIRATION_DAYS: Annotated[int, 1, 365] = 7
    TOKEN_ALGORITHM: Literal["HS256", "RS256"] = "HS256"

# Customize your config values here
Config = _ConfigClass()