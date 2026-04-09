"""Pydantic Models für das Krankenhaus."""
from typing import Final

from krankenhaus.entity import Krankenhaus
from krankenhaus.router import AdresseModel, FachbereichModel, KrankenhausUpdateModel

__all__: list[str] = ["KrankenhausModel"]


class KrankenhausModel(KrankenhausUpdateModel):
    """Pydantic Model für das Krankenhaus."""

    adresse: AdresseModel
    """Der zugehörige Name des Krankenhauses."""

    fachbereiche: list[FachbereichModel]
    """Die zugehörigen Fachbereiche des Krankenhauses."""

    def to_krankenhaus(self) -> Krankenhaus:
        """Konvertiert das Pydantic Model in ein Krankenhaus Entity.

        :return: Krankenhaus-Objekt für SQLAlchemy
        :rtype: Krankenhaus
        """
        krankenhaus_dict = self.to_dict()

        krankenhaus: Final = Krankenhaus(**krankenhaus_dict)
        krankenhaus.adresse = self.adresse.to_adresse()
        krankenhaus.fachbereiche = [
            fachbereich_model.to_fachbereich() for
            fachbereich_model in self.fachbereiche
        ]
        return krankenhaus
