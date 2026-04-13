"""Schema für GraphQL durch Strawberry."""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from krankenhaus.config.graphql import graphql_ide
from krankenhaus.graphql_api.graphql_types import Suchparameter
from krankenhaus.repository import KrankenhausRepository, Pageable
from krankenhaus.security import AuthorizationError, TokenService
from krankenhaus.service import KrankenhausDTO, KrankenhausService, NotFoundError

__all__ = ["Query", "get_context", "graphql_router", "schema"]


_repo: Final = KrankenhausRepository()
_service: Final = KrankenhausService(repo=_repo)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """Queries um Krankenhausdaten zu lesen."""

    @strawberry.field
    def krankenhaus(
        self,
        krankenhaus_id: strawberry.ID,
        info: Info,
    ) -> KrankenhausDTO | None:
        """Daten zu einem Krankenhaus lesen."""
        logger.debug("krankenhaus_id={}", krankenhaus_id)

        request: Final[Request] = info.context.get("request")
        try:
            _token_service.get_user_from_request(request=request)
        except AuthorizationError:
            return None

        try:
            krankenhaus_dto: Final = _service.find_by_id(
                krankenhaus_id=int(krankenhaus_id)
            )
        except NotFoundError:
            return None

        logger.debug("{}", krankenhaus_dto)
        return krankenhaus_dto

    @strawberry.field
    def krankenhaeuser(
        self,
        suchparameter: Suchparameter,
        info: Info,
    ) -> Sequence[KrankenhausDTO]:
        """Krankenhäuser anhand von Suchparametern suchen."""
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        try:
            _token_service.get_user_from_request(request=request)
        except AuthorizationError:
            return []

        suchparameter_dict: Final[dict[str, str | int]] = dict(vars(suchparameter))
        suchparameter_filtered: Final[dict[str, str]] = {
            key: str(value)
            for key, value in suchparameter_dict.items()
            if value is not None and value
        }
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            krankenhaeuser_dto: Final = _service.find(
                suchparameter=suchparameter_filtered,
                pageable=pageable,
            )
        except NotFoundError:
            return []

        logger.debug("{}", krankenhaeuser_dto)
        return krankenhaeuser_dto.content


schema: Final = strawberry.Schema(query=Query)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    """Request von FastAPI an den Strawberry-Kontext weiterreichen."""
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema,
    context_getter=get_context,
    graphql_ide=graphql_ide,
)
