"""Geschäftslogik zum lesen von Krnankenhausdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger

from krankenhaus.repository import KrankenhausRepository, Session
from krankenhaus.repository.pageable import Pageable
from krankenhaus.repository.slice import Slice
from krankenhaus.service import KrankenhausDTO, NotFoundError

__all__: list[str] = ["KrankenhausService"]


class KrankenhausService:
    """Service-Klasse für Krankenhaus."""

    def __init__(self, repo: KrankenhausRepository) -> None:
        """Konstruktor von KrankenhausService."""
        self._repo = repo

    def find_by_id(self, krankenhaus_id: int) -> KrankenhausDTO:
        """Such mit der Krankenhaus-ID.

        :param krankenhaus_id: ID des gesuchten Krankenhauses
        :return: KrankenhausDTO-Objekt
        :raises NotFoundError: Falls kein Krankenhaus gefunden wurde
        """
        logger.debug("krankenhaus_id={}", krankenhaus_id)

        with Session() as session:
            if (
                krankenhaus := self._repo.find_by_id(
                    krankenhaus_id=krankenhaus_id,
                    session=session,
                )
            ) is None:
                raise NotFoundError(krankenhaus_id=krankenhaus_id)

            krankenhaus_dto: Final = KrankenhausDTO(krankenhaus)

        logger.debug("krankenhaus_dto={}", krankenhaus_dto)
        return krankenhaus_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[KrankenhausDTO]:
        """Krankenhäuser mit Suchparametern suchen.

        :param suchparameter: Suchparameter
        :param pageable: Pageable-Objekt mit Seitennummer und Anzahl pro Seite
        :return: Gefundene Krankenhäuser
        :raises NotFoundError: Falls keine Krankenhäuser gefunden wurden
        """
        logger.debug("suchparameter={}", suchparameter)

        with Session() as session:
            krankenhaus_slice: Final = self._repo.find(
                suchparameter=suchparameter,
                pageable=pageable,
                session=session,
            )
            if len(krankenhaus_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            krankenhaeuser_dto: Final = tuple(
                KrankenhausDTO(krankenhaus) for krankenhaus in krankenhaus_slice.content
            )

        krankenhaeuser_dto_slice: Final = Slice(
            content=krankenhaeuser_dto,
            total_elements=krankenhaus_slice.total_elements,
        )
        logger.debug("krankenhaeuser_dto_slice={}", krankenhaeuser_dto_slice)
        return krankenhaeuser_dto_slice

    def find_namen(self, teil: str) -> Sequence[str]:
        """Krankenhausnamen zu einem Teilstring suchen.

        :param teil: Teilstring der gesuchten Namen
        :return: Gefundene Krankenhausnamen
        :raises NotFoundError: Falls keine Namen gefunden wurden
        """
        logger.debug("teil={}", teil)

        with Session() as session:
            namen: Final = self._repo.find_namen(teil=teil, session=session)

        if len(namen) == 0:
            raise NotFoundError(suchparameter={"name": teil})

        logger.debug("namen={}", namen)
        return namen
