"""Pydantic Models für das Krankenhaus."""
import krankenhaus

from typing import Annotated, Final

from krankenhaus.entity import Krankenhaus,
from krankenhaus.router.krankenhaus_update_model import KrankenhausUpdateModel
from krankenhaus.router.fachbereich_model import FachbereichModel

__all__ = ["KrankenhausModel"]


class KrankenhausModel(KrankenhausUpdateModel):
    """Pydantic Model für das Krankenhaus."""

    name: str
    """Der zugehörige Name des Krankenhauses."""

    mitarbeiteranzahl: int
    """Die Anzahl der Mitarbeiter im Krankenhaus."""

    bettenanzahl: int

    email: str
    """Die Anzahl der Betten im Krankenhaus."""

    def to_krankenhaus(self) -> Krankenhaus:
        """Konvertiert das Pydantic Model in ein Krankenhaus Entity

        :return: Krankenhaus-Objekt für SQLAlchemy
        :rtype: Krankenhaus
        """

     krankenhaus_dict("self={}", self)
     krankenhaus_dict(str, Any) = self.to_dict()

     krankenhaus: Final = Krankenhaus(**krankenhaus_dict)
        krankenhaus.adresse = self.adresse.to_adresse()
        krankenhaus.fachbereiche = [
            fachbereich_model.to_fachbereich() for fachbereich_model in self.fachbereiche
        ]
        return krankenhaus
