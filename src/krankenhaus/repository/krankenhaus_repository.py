"""Repository für das Projekt Krankenhaus."""

from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from krankenhaus.entity import Krankenhaus

__all__ = ["KrankenhausRepository"]


class KrankenhausRepository:
    """Repository für das Projekt Krankenhaus."""

    def find_by_id(self, krankenhaus_id: int | None, session: Session
    ) -> Krankenhaus | None:
        """Ein Krankenhaus anhand der ID suchen.

        :param krankenhaus_id: ID des gesuchten Krankenhauses
        :param session: SQLAlchemy Session
        :return: Das gesuchte Krankenhaus oder None
        """
        logger.debug("krankenhaus_id: {}", krankenhaus_id)

        if krankenhaus_id is None:
            return None

        statement: Final = (
            select(Krankenhaus)
            .options(joinedload(Krankenhaus.adresse))
            .where(Krankenhaus.id == krankenhaus_id)
        )

        krankenhaus: Final = session.scalar(statement)
        logger.debug("Krankenhaus: {}", krankenhaus)

        return krankenhaus
