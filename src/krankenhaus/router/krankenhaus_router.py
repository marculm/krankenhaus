
"""KrankenhausGetRouter."""
from dataclasses import asdict
from rich.json import JSON

from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from krankenhaus.repository import Pageable
from krankenhaus.repository.slice import Slice
from krankenhaus.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from krankenhaus.router.dependencies import get_service
from krankenhaus.router.page import Page
from krankenhaus.security import Role, RolesRequired, User
from krankenhaus.service import KrankenhausDTO, KrankenhausService, KrankenhausDTO, KrankenhausService

__all__: list[str] = ["krankenhaus_router"]


krankenhaus_router: Final = APIRouter(tags=["Lesen"])

@krankenhaus_router.get(  # noqa: E302
    path="/{krankenhaus_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def get_by_id(
    krankenhaus_id: int,
    request: Request,
    service: Annotated[KrankenhausService, Depends(get_service)],
) -> Response:
    """Liest ein Krankenhaus anhand der ID aus der Datenbank.

    :param krankenhaus_id: Die ID des Krankenhauses
    :type krankenhaus_id: int
    :param request: Das HTTP-Request-Objekt
    :type request: Request
    :param response: Das HTTP-Response-Objekt
    :type response: Response
    :return: Das Krankenhaus-Objekt oder eine Fehlermeldung
    :rtype: Any
    """
    krankenhaus: Final= service.get_by_id(krankenhaus_id=krankenhaus_id)  # noqa: E225

    if_none_match: Final = request.headers.get("if-none-match")
    if (
        if_none_match is not None
        and len(if_none_match) > IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version: str = if_none_match[1:-1]
        if version is not None:
            try:
                if int(version) == krankenhaus.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                pass
    return JSONResponse(
        content=_krankenhaus_to_dict(krankenhaus),
        headers={ETAG: f'"{krankenhaus.version}"'},
    )


def _krankenhaus_to_dict(krankenhaus: KrankenhausDTO) -> dict[str, Any]:
    krankenhaus_dict: Final = asdict(obj=krankenhaus)
    krankenhaus_dict.pop("version")
    return krankenhaus_dict
