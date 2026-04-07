"""DTO-Klasse für die Adresse."""

from dataclasses import dataclass

from krankenhaus.entity.adresse import Adresse


@dataclass(eq=False, slots=True, kw_only=True)
class AdresseDTO:
    """Data Transfer Object für die Adresse."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str

    def __init__(self, adresse: Adresse):
        """AdresseDTO aus Adresse erstellen."""
        self.strasse = adresse.strasse
        self.hausnummer = adresse.hausnummer
        self.plz = adresse.plz
        self.ort = adresse.ort
