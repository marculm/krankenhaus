"""KrankenhausGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from krankenhaus.repository.slice import Slice
from krankenhaus.router.page import Page
from rich.json import JSON

from krankenhaus.repository import Pageable
from krankenhaus.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from krankenhaus.router.dependencies import get_service
from krankenhaus.security import Role, RolesRequired
from krankenhaus.service import KrankenhausDTO, KrankenhausService

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

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
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


def get(
    request: Request,
    service: Annotated[KrankenhausService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter.

    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit Query-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit einer Seite mit Patienten-Daten
    :rtype: Response
    :raises NotFoundError: Falls keine Patienten gefunden wurden
    """
    query_params: Final = request.query_params

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    krankenhaus_slice: Final = service.find(
        suchparameter=suchparameter, pageable=pageable)

    result: Final = _krankenhaus_slice_to_page(krankenhaus_slice, pageable)
    return JSONResponse(content=result)

    def _krankenhaus_slice_to_page(
    patient_slice: Slice[KrankenhausDTODTO],
    pageable: Pageable,
) -> dict[str, Any]:
    krankenhaus_dict: Final = tuple(
        _krankenhaus_to_dict(krankenhaus) for krankenhaus in krankenhaus_slice.content
    )
    page: Final = Page.create(
        content=krankenhaus_dict,
        pageable=pageable,
        total_elements=krankenhaus_slice.total_elements,
    )
    return asdict(obj=page)


def _krankenhaus_to_dict(krankenhaus: KrankenhausDTO) -> dict[str, Any]:
    krankenhaus_dict: Final = asdict(obj=krankenhaus)
    krankenhaus_dict.pop("version")
    return krankenhaus_dict
