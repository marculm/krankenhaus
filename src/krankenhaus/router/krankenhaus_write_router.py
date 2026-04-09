"""KrankenhausWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from krankenhaus.router import KrankenhausModel
from krankenhaus.router.dependencies import get_write_service
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
    :return: Eine leere Antwort mit Statuscode 201 Created
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
