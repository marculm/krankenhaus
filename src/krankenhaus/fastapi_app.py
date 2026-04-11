"""MainApp."""

from contextlib import asynccontextmanager
from time import time
from typing import TYPE_CHECKING, Final

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from krankenhaus.banner import banner
from krankenhaus.config import (
    dev_db_populate,
    dev_keycloak_populate,
)
from krankenhaus.config.dev.db_populate import db_populate
from krankenhaus.config.dev.db_populate_router import router as db_populate_router
from krankenhaus.config.dev.keycloak_populate_router import (
    router as keycloak_populate_router,
)
from krankenhaus.problem_details import create_problem_details
from krankenhaus.repository.session_factory import engine
from krankenhaus.router import (
    health_router,
    krankenhaus_router,
    krankenhaus_write_router,
    shutdown_router,
)
from krankenhaus.security import AuthorizationError, LoginError
from krankenhaus.security import router as auth_router
from krankenhaus.service import (
    EmailExistsError,
    NotFoundError,
    VersionOutdatedError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable

__all__ = [
    "authorization_error_handler",
    "email_exists_error_handler",
    "login_error_handler",
    "not_found_error_handler",
    "version_outdated_error_handler",
]


TEXT_PLAIN: Final = "text/plain"


# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
# https://fastapi.tiangolo.com/advanced/events
# pylint: disable=redefined-outer-name
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """DB und Keycloak neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        db_populate()
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: Final = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(GZipMiddleware, minimum_size=500)  # ty:ignore[invalid-argument-type]


@app.middleware("http")
async def log_request_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    logger.debug(f"{request.method} '{request.url}'")
    return await call_next(request)


@app.middleware("http")
async def log_response_time(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000
    logger.debug(
        f"Response time: {duration_ms:.2f} ms, statuscode: {response.status_code}"
    )
    return response


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(krankenhaus_router, prefix="/rest")
app.include_router(krankenhaus_write_router, prefix="/rest")
app.include_router(auth_router, prefix="/auth")
app.include_router(health_router, prefix="/health")
app.include_router(shutdown_router, prefix="/admin")

if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")


# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------
@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError.

    :param _err: NotFoundError aus der Geschäftslogik
    :return: Response mit Statuscode 404
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(AuthorizationError)
def authorization_error_handler(
    _request: Request,
    _err: AuthorizationError,
) -> Response:
    """Errorhandler für AuthorizationError.

    :param _err: AuthorizationError vom Extrahieren der Benutzerkennung aus dem
        Authorization-Header
    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(LoginError)
# pylint: disable-next=invalid-name
def login_error_handler(_request: Request, err: LoginError) -> Response:
    """Exception-Handler, wenn der Benutzername oder das Passwort fehlerhaft ist.

    :param _exc: LoginError
    :return: Response-Objekt mit Statuscode 401
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
    )


@app.exception_handler(EmailExistsError)
def email_exists_error_handler(_request: Request, err: EmailExistsError) -> Response:
    """Exception-Handling für EmailExistsError.

    :param err: Exception, falls die Emailadresse des neuen oder zu ändernden Patienten
        bereits existiert
    :return: Response mit Statuscode 422
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError.

    :param _err: Exception, falls die Versionsnummer zum Aktualisieren veraltet ist
    :return: Response mit Statuscode 412
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )
