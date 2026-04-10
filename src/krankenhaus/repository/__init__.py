"""Modul für den Datenbankzugriff im Projekt Krankenhaus."""

from .krankenhaus_repository import KrankenhausRepository
from .pageable import MAX_PAGE_SIZE, Pageable
from .session_factory import Session, engine
from .slice import Slice

__all__: list[str] = [
    "MAX_PAGE_SIZE",
    "KrankenhausRepository",
    "Pageable",
    "Session",
    "Slice",
    "engine"
]
