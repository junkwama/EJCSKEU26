# External modules
import re
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from modules.oauth2.dependencies import get_token_payload_dependency

# Loading critic stuff needed accross diff local modules
from dotenv import load_dotenv
from core.config import Config
load_dotenv()

# Routers utils
from routers.utils.http_utils import (
    send200,
    send404,
    send500,
    send422,
    send409,
    send403,
    send401,
)

# models
from models.oauth import TokenPayload

# Routers
from routers.fidele import fidele_router
from routers.paroisse import paroisse_router
from routers.adresse import adresse_router
from routers.contact import contact_router
from routers.direction import direction_router
from routers.constant import constant_router
from routers.oauth import oauth_router
from routers.superadmin import superadmin_router

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    yield
    # Shutdown code 
    print("Shutting down...")

app = FastAPI(
    title="EJCSK API",
    description="Recencement des Fidèles de l'Église Kimbaguiste",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Depends(get_token_payload_dependency(TokenPayload))],
) # The app's fastweb instance

app.add_middleware(
    CORSMiddleware,
    allow_origins= Config.ALLOWED_ORIGINS.value,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 401: Uncontroled or automatically generated
@app.exception_handler(401)
def exc_handler_401(request: Request, e: HTTPException):
    return send401(str(e) or None)

# 403: Uncontroled or automatically generated
@app.exception_handler(403)
def exc_handler_403(request: Request, e: HTTPException):
    return send403(str(e) or None)

# 404: Resource not found
@app.exception_handler(404)
def exc_handler_404(request: Request, e: HTTPException):
    return send404(["path"], str(e) or "Resource not found")

def _extract_duplicate_error_details(error: IntegrityError) -> tuple[str | None, str | None]:
    raw_message = str(getattr(error, "orig", error))

    # MySQL/MariaDB format: Duplicate entry 'x' for key 'y'
    mysql_match = re.search(r"Duplicate entry '(.+)' for key '([^']+)'", raw_message)
    if mysql_match:
        value = mysql_match.group(1)
        key = mysql_match.group(2).split(".")[-1]
        return key, value

    # SQLite format: UNIQUE constraint failed: table.col, table.col
    sqlite_match = re.search(r"UNIQUE constraint failed: (.+)", raw_message)
    if sqlite_match:
        columns = sqlite_match.group(1)
        first_col = columns.split(",")[0].strip().split(".")[-1]
        return first_col, None

    return None, None


def _is_duplicate_conflict_message(raw_message: str) -> bool:
    lowered = raw_message.lower()
    return (
        "duplicate entry" in lowered
        or "unique constraint failed" in lowered
        or "duplicate principale" in lowered
    )


# 409 DB duplicate/unique conflict
@app.exception_handler(IntegrityError)
def exc_handler_409(request: Request, e: IntegrityError):
    err_key, err_value = _extract_duplicate_error_details(e)
    if err_key:
        loc = (
            "path"
            if err_key in request.path_params
            else "query" if err_key in request.query_params else "body"
        )
        message = (
            f"'{err_value}' as '{err_key}' is already used."
            if err_value is not None
            else f"'{err_key}' is already used."
        )
        return send409([loc, err_key], message)

    return send409(["body", "database"], "Duplicate value conflict")


@app.exception_handler(OperationalError)
def exc_handler_409_operational(request: Request, e: OperationalError):
    raw_message = str(getattr(e, "orig", e))
    if _is_duplicate_conflict_message(raw_message):
        return send409(["body", "database"], "Duplicate value conflict")
    return send500(e)


# 422 Pydantic check fails
@app.exception_handler(RequestValidationError)
def exc_handler_422(request: Request, e: RequestValidationError):
    return send422(exception=e)


# Exceptions reprocessed and formated bfr bein' sent to the client
# General 500 exceptions
@app.exception_handler(Exception)
def exc_handler_500(
    request: Request, e: Exception
):  # NB: even when we don't use request we must put it because the func expects it
    if isinstance(e, (RequestValidationError, ValidationError)):
        return exc_handler_422(
            request, e
        )  # Delegate to 422 handler as Beanie may fail to throw the right errors
    return send500(e)


@app.get("/")
def server_status():
    return send200(
        {
            "app_name": "ejcsk api",
            "version": "1.0.0",
            "status": "Server up running",
            "status_code": 200,
        }
    )

# Attaching routers
app.include_router(oauth_router, prefix="/oauth", tags=["Oauth"])

app.include_router(fidele_router, prefix="/fidele")
app.include_router(paroisse_router, prefix="/paroisse")
app.include_router(direction_router, prefix="/direction")

app.include_router(adresse_router, prefix="/adresse")
app.include_router(contact_router, prefix="/contact")
app.include_router(constant_router, prefix="/constant")
app.include_router(superadmin_router, prefix="/superadmin")


# start the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
