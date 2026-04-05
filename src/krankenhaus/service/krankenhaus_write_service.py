"""Write Service für das Projekt Krankenhaus."""

from typing import Final

from loguru import logger
from sqlalchemy.orm import Session

from krankenhaus.entity import Krankenhaus
from krankenhaus.repository import KrankenhausRepository
from krankenhaus.service import EmailExistsError, KrankenhausDTO

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
