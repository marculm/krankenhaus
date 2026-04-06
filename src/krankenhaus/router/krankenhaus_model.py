"""Pydantic Models for Krankenhaus Data."""


from typing import Annotated, Final
from krankenhaus.entity import Krankenhaus
from krankenhaus.entity import Krankenhaus, Adresse, Fachbereich
from krankenhaus.router.krankenhaus_update_model import KrankennhausUpdateModel

__all__: list[str] = ["KrankenhausModel"]

class KrankenhausModel(KrankenhausUpdateModel):
    """Pydantic Model für Krankenhaus Daten."""

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

        krankenhaus_dict: dict[str, Any] = self.to_dict()
        krankenhaus_dict(str, Any) = self.to_dict()

        krankenhaus: Final = Krankenhaus(**krankenhaus_dict)
        krankenhaus.adresse: Adresse = self.adresse.to_adresse()
        krankenhaus.fachbereich: list[Fachbereich] = [
            fachbereich_model.to_fachbereich() for
            fachbereich_model in self.fachbereich
        ]
        return krankenhaus
