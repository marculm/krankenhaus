"""Modul für den Geschäftslogik im Projekt Krankenhaus."""

from .adresse_dto import AdresseDTO
from .exceptions import EmailExistsError, NotFoundError, VersionOutdatedError
from .krankenhaus_dto import KrankenhausDTO

__all__: list[str] = [
    "AdresseDTO",
    "EmailExistsError",
    "KrankenhausDTO",
    "NotFoundError",
    "VersionOutdatedError"
]
