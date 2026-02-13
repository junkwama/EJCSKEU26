# External modules
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from contextlib import asynccontextmanager
from pydantic import ValidationError

# Loading critic stuff needed accross diff local modules
from dotenv import load_dotenv
load_dotenv()


# Routers utils
from routers.utils.http_utils import (
    send200,
    send404,
    send500,
    send422,
    # send409,
    send403,
    send401,
)

# Routers
from routers.fidele import fidele_router
from routers.paroisse import paroisse_router
from routers.adresse import adresse_router
from routers.contact import contact_router
from routers.direction import direction_router
from routers.constant import constant_router

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
    lifespan=lifespan
) # The app's fastweb instance

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

# # 409 DB Unique Key Duplication Error
# @app.exception_handler(DuplicateKeyError)
# def exc_handler_409(request: Request, e: DuplicateKeyError):
#     # get the 1st conflict key
#     errKey, errValue = list(e._OperationFailure__details["keyValue"].items())[0]
#     loc = (
#         "path"
#         if errKey in request.path_params
#         else "query" if errKey in request.query_params else "body"
#     )
#     return send409([loc, errKey], f"'{errValue}' as '{errKey}' is already used.")


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
app.include_router(fidele_router, prefix="/fidele")
app.include_router(paroisse_router, prefix="/paroisse")
app.include_router(direction_router, prefix="/direction")

app.include_router(adresse_router, prefix="/adresse")
app.include_router(contact_router, prefix="/contact")
app.include_router(constant_router, prefix="/constant")


# start the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="info")
