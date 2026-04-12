"""KrankenhausWriteRouter."""
from krankenhaus.security import RolesRequired, Role

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from krankenhaus.problem_details import create_problem_details
from krankenhaus.router.constants import IF_MATCH_MIN_LEN
from krankenhaus.router.dependencies import get_write_service
from krankenhaus.router.krankenhaus_model import KrankenhausModel
from krankenhaus.router.krankenhaus_update_model import KrankenhausUpdateModel
from krankenhaus.service import KrankenhausWriteService

__all__ = ["krankenhaus_write_router"]


krankenhaus_write_router: Final = APIRouter(tags=["Schreiben"])


@krankenhaus_write_router.post("")
def post(
    krankenhaus_model: KrankenhausModel,
    request: Request,
    service: Annotated[KrankenhausWriteService, Depends(get_write_service)],
) -> Response:
    """Erstellt ein neues Krankenhaus.

    :param krankenhaus_model: Das Krankenhaus, das erstellt werden soll
    :type krankenhaus_model: KrankenhausModel
    :param request: Die HTTP-Anfrage
    :type request: Request
    :param service: Der Service für die Geschäftslogik
    :type service: KrankenhausWriteService
    :rtype: Response
    """
    logger.debug("krankenhaus_model={}", krankenhaus_model)
    krankenhaus_dto: Final = service.create(
        krankenhaus=krankenhaus_model.to_krankenhaus()
    )
    logger.debug("krankenhaus_dto={}", krankenhaus_dto)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{krankenhaus_dto.id}"},
    )


@krankenhaus_write_router.put(
    "/{id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.KRANKENHAUS]))]
)
def put(
    krankenhaus_id: int,
    krankenhaus_update_model: KrankenhausUpdateModel,
    request: Request,
    service: Annotated[KrankenhausWriteService, Depends(get_write_service)]
) -> Response:
    """Aktualisiert ein bestehendes Krankenhaus.

    :param krankenhaus_id: Die ID des zu aktualisierenden Krankenhauses
    :type krankenhaus_id: int
    :param krankenhaus_update_model: Das Krankenhaus mit den aktualisierten Daten
    :type krankenhaus_update_model: KrankenhausUpdateModel
    :param request: Die HTTP-Anfrage
    :type request: Request
    :param service: Der Service für die Geschäftslogik
    :type service: KrankenhausWriteService
    :rtype: Response
    """
    if_match_value = request.headers.get("If-Match")
    logger.debug(
        "krankenhaus_id={}, krankenhaus_update_model={}, if_match={}",
        krankenhaus_id,
        krankenhaus_update_model,
        if_match_value
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    krankenhaus: Final = krankenhaus_update_model.to_krankenhaus()
    krankenhaus_modified: Final = service.update(
        krankenhaus_id=krankenhaus_id,
        krankenhaus=krankenhaus,
        version=version_int
    )
    logger.debug("krankenhaus_modified={}", krankenhaus_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{krankenhaus_modified.version}"'},
        )


@krankenhaus_write_router.delete(
    "/{id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.KRANKENHAUS]))]
)
def delete_by_id(
    krankenhaus_id: int,
    service: Annotated[KrankenhausWriteService, Depends(get_write_service)]
) -> Response:
    """Löscht ein Krankenhaus anhand der ID.

    :param krankenhaus_id: Die ID des zu löschenden Krankenhauses
    :type krankenhaus_id: int
    :param request: Die HTTP-Anfrage
    :type request: Request
    :param service: Der Service für die Geschäftslogik
    :type service: KrankenhausWriteService
    :rtype: Response
    """
    logger.debug("krankenhaus_id={}", krankenhaus_id)
    service.delete_by_id(krankenhaus_id=krankenhaus_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
