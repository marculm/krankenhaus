"""Write Service für das Projekt Krankenhaus."""

from typing import Final

from loguru import logger
from sqlalchemy.orm import Session

from krankenhaus.entity import Krankenhaus
from krankenhaus.repository import KrankenhausRepository
from krankenhaus.service import (
    EmailExistsError,
    KrankenhausDTO,
    NotFoundError,
    VersionOutdatedError,
)

__all__ = ["KrankenhausWriteService"]


class KrankenhausWriteService:
    """Write Service für das Projekt Krankenhaus."""

    def __init__(self, repo: KrankenhausRepository) -> None:
        """Initialisierung des KrankenhausWriteService."""
        self.repo = repo

    def create(self, krankenhaus: Krankenhaus) -> KrankenhausDTO:
        """Ein neues Krankenhaus erstellen.

        :param krankenhaus: Das zu erstellende Krankenhaus
        :return: Das erstellte Krankenhaus mit ID
        """
        logger.debug(
            "krankenhaus={}, adresse={}, fachbereiche={}",
            krankenhaus,
            krankenhaus.adresse,
            krankenhaus.fachbereiche,
        )

        with Session() as session:
            if self.repo.email_exists(krankenhaus.email, session):
                raise EmailExistsError(krankenhaus.email)

            krankenhaus_db: Final = self.repo.create(krankenhaus, session)
            krankenhaus_dto: Final = KrankenhausDTO(krankenhaus_db)
            session.commit()

        logger.debug("krankenhaus_dto: {}", krankenhaus_dto)
        return krankenhaus_dto

    def update(
            self, krankenhaus: Krankenhaus, krankenhaus_id: int, version: int
        ) -> KrankenhausDTO:
        """Ein bestehendes Krankenhaus aktualisieren.

        :param krankenhaus_id: ID des zu aktualisierenden Krankenhauses
        :param krankenhaus: Das Krankenhaus mit den neuen Daten
        :param version: Die aktuelle Versionsnummer des Krankenhauses
        :return: Das aktualisierte Krankenhaus
        """
        logger.debug("krankenhaus_id={}, version={}", krankenhaus_id, version)

        with Session() as session:
            if (
                krankenhaus_db := self.repo.find_by_id(krankenhaus_id, session)
            ) is None:
                raise NotFoundError(krankenhaus.id)
            if krankenhaus_db.version > version:
                raise VersionOutdatedError(version)

            email: Final = krankenhaus.email
            if (
                email != krankenhaus_db.email and
                self.repo.email_exists_for_other_id(email, krankenhaus_id, session)
            ):
                raise EmailExistsError(email)

            krankenhaus_db.set(krankenhaus)
            if (krankenhaus_db := self.repo.update(krankenhaus_db, session)) is None:
                raise NotFoundError(krankenhaus_id)

            krankenhaus_dto: Final = KrankenhausDTO(krankenhaus_db)
            logger.debug("krankenhaus_dto: {}", krankenhaus_dto)
            session.commit()

            krankenhaus_dto.version += 1
            return krankenhaus_dto

    def delete_by_id(self, krankenhaus_id: int) -> None:
        """Ein Krankenhaus anhand der ID löschen.

        :param krankenhaus_id: ID des zu löschenden Krankenhauses
        """
        logger.debug("krankenhaus_id: {}", krankenhaus_id)

        with Session() as session:
            if self.repo.find_by_id(krankenhaus_id, session) is None:
                raise NotFoundError(krankenhaus_id)

            self.repo.delete_by_id(krankenhaus_id, session)
            session.commit()
