"""DTO-KLasse für Krankenhaus."""

from dataclasses import dataclass

import strawberry

from krankenhaus.entity import Krankenhaus
from krankenhaus.service import AdresseDTO

__all__: list[str] = ["KrankenhausDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class KrankenhausDTO:
    """DTO-Klasse für Krankenhaus."""

    id: int
    version: int
    name: str
    mitarbeiteranzahl: int
    bettenanzahl: int
    email: str
    adresse: AdresseDTO

    def __init__(self, krankenhaus: Krankenhaus):
        """Initialisierung von KrankenhausDTO durch ein Entity-Objekt von Krankenhaus.

        :param krankenhaus: Krankenhaus-Objekt mit den Decorators zu SQLAlchemy
        """
        krankenhaus_id: int | None = krankenhaus.id
        self.id: int = krankenhaus_id if krankenhaus_id is not None else -1
        self.version: int = krankenhaus.version
        self.name: str = krankenhaus.name
        self.mitarbeiteranzahl: int = krankenhaus.mitarbeiteranzahl
        self.bettenanzahl: int = krankenhaus.bettenanzahl
        self.email: str = krankenhaus.email
        self.adresse = AdresseDTO(krankenhaus.adresse)
