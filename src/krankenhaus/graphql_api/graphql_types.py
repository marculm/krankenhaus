"""Schema für GraphQL."""

import strawberry

__all__ = ["Suchparameter"]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Krankenhäusern."""

    name: str | None = None
    """Name als Suchkriterium."""

    email: str | None = None
    """Emailadresse als Suchkriterium."""

    mitarbeiteranzahl: int | None = None
    """Mitarbeiteranzahl als Suchkriterium."""

    bettenanzahl: int | None = None
    """Bettenanzahl als Suchkriterium."""
