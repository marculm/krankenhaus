"""Pydandic-Model zum Aktualisieren von Krankenhausdaten."""
from pydantic import BaseModel

__all__ = ["KrankenhausUpdateModel"]


class KrankenhausUpdateModel(BaseModel):
    """Pydantic Model zum Aktualisieren von Krankenhausdaten."""

    name: str
    """Der zugehörige Name des Krankenhauses."""

    mitarbeiteranzahl: int
    """Die Anzahl der Mitarbeiter im Krankenhaus."""

    bettenanzahl: int

    email: str
    """Die Anzahl der Betten im Krankenhaus."""
