"""Repository für das Projekt Krankenhaus."""

from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from krankenhaus.entity import Krankenhaus
from krankenhaus.repository.pageable import Pageable
from krankenhaus.repository.slice import Slice

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

    def find_all(self, pageable: Pageable, session: Session) -> Slice[Krankenhaus]:
        """Alle Krankenhäuser mit Pagination suchen.

        :param pageable: Pageable-Objekt mit Seitennummer und Anzahl pro Seite
        :param session: SQLAlchemy Session
        :return: Liste der gefundenen Krankenhäuser
        """
        statement: Final = (
            (
                select(Krankenhaus)
                .options(joinedload(Krankenhaus.adresse))
                .offset(pageable.number * pageable.size)
                .limit(pageable.size)
            )
            if pageable.size != 0
            else (select(Krankenhaus).options(joinedload(Krankenhaus.adresse)))
        )

        krankenhaeuser: Final = session.scalars(statement).all()
        logger.debug("Krankenhäuser: {}", krankenhaeuser)
        anzahl: Final = self._count_all_rows(session)
        krankenhaus_slice: Final = Slice(
            content=tuple(krankenhaeuser), total_elements=anzahl
        )
        return krankenhaus_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Krankenhaus)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0
