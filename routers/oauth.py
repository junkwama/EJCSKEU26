# External modules
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import ValidationError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Local modules
from core.db import get_session
from models.fidele import Fidele
from models.oauth import OauthModel

from models.utils.utils import Password
from modules.oauth2.models import AccessToken

from routers.utils.http_utils import send401, send422

oauth_router = APIRouter()

@oauth_router.post("")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AccessToken:
    """ 
    Returns:\n
        200: Fidele authentificated and sends back a AccessToken object
        401: If the password or username (main phone number) is incorect
        422: If the password or the username doesn't have the right the format
    """
    
    # Fastapi automatically catches only pydantic errors occured in the route's function's params. 
    # For the others we need to catch them otherwise they log some errors
    fidele_auth = None
    try:
        fidele_auth = OauthModel(username=form_data.username, password=form_data.password)
    except (ValidationError, ValueError) as e:
        return send422(exception=e)

    statement = select(Fidele).where(Fidele.tel == fidele_auth.username)
    result = await session.exec(statement)
    fidele = result.first()

    if not fidele or not Password.check(fidele_auth.password, fidele.password):
        return send401(error_message="Password or username incorrect") 
    token = AccessToken(access_token=fidele.generate_token())
    # This route must respect an external "returned data" format to comply with oauth2
    return token
