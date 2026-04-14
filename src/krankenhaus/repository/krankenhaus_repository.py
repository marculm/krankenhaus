"""Repository für das Projekt Krankenhaus."""

from collections.abc import Mapping, Sequence
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

    def find_by_id(
        self, krankenhaus_id: int | None, session: Session
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

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Krankenhaus]:
        """Krankenhäuser anhand von Suchparametern suchen.

        :param suchparameter: Suchparameter aus der Query
        :param pageable: Pageable-Objekt mit Seitennummer und Anzahl pro Seite
        :param session: SQLAlchemy Session
        :return: Liste der gefundenen Krankenhäuser
        """
        logger.debug("suchparameter: {}", suchparameter)

        conditions = []

        if name := suchparameter.get("name"):
            conditions.append(Krankenhaus.name.ilike(f"%{name}%"))
        if email := suchparameter.get("email"):
            conditions.append(Krankenhaus.email.ilike(f"%{email}%"))
        if (mitarbeiteranzahl := suchparameter.get("mitarbeiteranzahl")) is not None:
            conditions.append(Krankenhaus.mitarbeiteranzahl == int(mitarbeiteranzahl))
        if (bettenanzahl := suchparameter.get("bettenanzahl")) is not None:
            conditions.append(Krankenhaus.bettenanzahl == int(bettenanzahl))

        statement = select(Krankenhaus).options(joinedload(Krankenhaus.adresse))
        count_statement = select(func.count()).select_from(Krankenhaus)
        if len(conditions) != 0:
            statement = statement.where(*conditions)
            count_statement = count_statement.where(*conditions)

        if pageable.size != 0:
            statement = statement.offset(pageable.number * pageable.size).limit(
                pageable.size,
            )

        krankenhaeuser: Final = session.scalars(statement).all()
        anzahl: Final = session.scalar(count_statement)
        krankenhaus_slice: Final = Slice(
            content=tuple(krankenhaeuser),
            total_elements=anzahl if anzahl is not None else 0,
        )
        logger.debug("krankenhaus_slice: {}", krankenhaus_slice)
        return krankenhaus_slice

    def find_namen(self, teil: str, session: Session) -> Sequence[str]:
        """Krankenhausnamen zu einem Teilstring suchen.

        :param teil: Teilstring der gesuchten Namen
        :param session: SQLAlchemy Session
        :return: Gefundene Krankenhausnamen
        """
        logger.debug("teil: {}", teil)

        statement: Final = (
            select(Krankenhaus.name)
            .where(Krankenhaus.name.ilike(f"%{teil}%"))
            .order_by(Krankenhaus.name)
        )
        namen: Final = tuple(session.scalars(statement).all())
        logger.debug("namen: {}", namen)
        return namen

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Krankenhaus)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def create(self, krankenhaus: Krankenhaus, session: Session) -> Krankenhaus:
        """Ein neues Krankenhaus abspeichern.

        :param krankenhaus: Krankenhaus-Objekt mit den Daten des neuen Krankenhauses
        :param session: SQLAlchemy Session
        :return: Das angelegte Krankenhaus mit ID
        """
        session.add(krankenhaus)
        session.flush([krankenhaus])
        logger.debug("krankenhaus_id: {}", krankenhaus.id)
        return krankenhaus

    def update(self, krankenhaus: Krankenhaus, session: Session) -> Krankenhaus | None:
        """Ein bestehendes Krankenhaus aktualisieren.

        :param krankenhaus: Krankenhaus-Objekt mit den aktualisierten Daten
        :param session: SQLAlchemy Session
        :return: Das aktualisierte Krankenhaus
        """
        logger.debug("krankenhaus: {}", krankenhaus)

        if (krankenhaus_db := self.find_by_id(krankenhaus.id, session)) is None:
            return None

        logger.debug("{}", krankenhaus)
        return krankenhaus_db

    def delete_by_id(self, krankenhaus_id: int, session: Session) -> None:
        """Ein Krankenhaus anhand der ID löschen.

        :param krankenhaus_id: ID des zu löschenden Krankenhauses
        :param session: SQLAlchemy Session
        """
        logger.debug("krankenhaus_id: {}", krankenhaus_id)

        if (krankenhaus_db := self.find_by_id(krankenhaus_id, session)) is None:
            return

        session.delete(krankenhaus_db)
        logger.debug("ok")

    def email_exists(self, email: str, session: Session) -> bool:
        """Prüfen, ob eine E-Mail-Adresse bereits existiert.

        :param email: E-Mail-Adresse, die geprüft werden soll
        :param session: SQLAlchemy Session
        :return: True, wenn die E-Mail-Adresse bereits existiert, sonst False
        """
        statement: Final = select(func.count()).where(Krankenhaus.email == email)
        anzahl: Final = session.scalar(statement)

        logger.debug("anzahl: {}", anzahl)
        return anzahl is not None and anzahl > 0

    def email_exists_for_other_id(
        self, email: str, krankenhaus_id: int, session: Session
    ) -> bool:
        """Prüfen, ob eine E-Mail-Adresse bereits bei einer anderen ID existiert.

        :param email: E-Mail-Adresse, die geprüft werden soll
        :param krankenhaus_id: ID des Krankenhauses, das ignoriert werden soll
        :param session: SQLAlchemy Session
        :return: True, wenn die E-Mail-Adresse bereits existiert, sonst False
        """
        logger.debug("email: {}", email)

        statement: Final = select(Krankenhaus.id).where(Krankenhaus.email == email)
        id_db: Final = session.scalar(statement)

        logger.debug("id_db: {}", id_db)
        return id_db is not None and id_db != krankenhaus_id
