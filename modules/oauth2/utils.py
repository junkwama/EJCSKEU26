from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from .config import Config

secury_scheme = OAuth2PasswordBearer(tokenUrl="oauth", auto_error=False)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAUTH_TOKEN_ERROR_CODE = 401
OAUTH_TOKEN_ERROR_MESS = "Authentification required"
OAUTH_INVALID_TOKEN_ERROR_MESS = "Token expired or invalid"

def get_token_exp(exp_delta_days: int | None = None) -> int:
  # Time stamp is a float with millisec in decimal part. We drop millisecs
  # To make token lighter
  exp = datetime.now() + timedelta(days=exp_delta_days or Config.TOKEN_EXPIRATION_DAYS)
  return int(exp.timestamp()) 