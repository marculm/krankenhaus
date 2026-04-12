"""Modul für den Geschäftslogik im Projekt Krankenhaus."""

from .adresse_dto import AdresseDTO
from .exceptions import (
    EmailExistsError,
    ForbiddenError,
    NotFoundError,
    VersionOutdatedError,
)
from .krankenhaus_dto import KrankenhausDTO
from .krankenhaus_service import KrankenhausService
from .krankenhaus_write_service import KrankenhausWriteService
from .mailer import send_mail

__all__: list[str] = [
    "AdresseDTO",
    "EmailExistsError",
    "ForbiddenError",
    "KrankenhausDTO",
    "KrankenhausService",
    "KrankenhausWriteService",
    "NotFoundError",
    "VersionOutdatedError",
    "send_mail",
]
