"""Entity-Klasse für das Krankenhaus."""
from datetime import datetime
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from krankenhaus.entity.adresse import Adresse
from krankenhaus.entity.base import Base
from krankenhaus.entity.fachbereich import Fachbereich


class Krankenhaus(Base):
    """Entity-Klasse für das Krankenhaus."""

    __tablename__ = "krankenhaus"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )

    name: Mapped[str]

    mitarbeiteranzahl: Mapped[int]

    bettenanzahl: Mapped[int]

    email: Mapped[str] = mapped_column(unique=True)

    fachbereiche: Mapped[list[Fachbereich]] = relationship(
        back_populates="krankenhaus",
        cascade="save-update, delete",
    )

    adresse: Mapped[Adresse] = relationship(
        back_populates="krankenhaus",
        innerjoin=True,
        cascade="save-update, delete",
    )

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleicheit, ohne Joins zu verursachen."""
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Krankenhauses als String, ohne Joins zu verursachen."""
        return (
            f"Krankenhaus(id={self.id!r}, name={self.name!r}, "
            + f"mitarbeiteranzahl={self.mitarbeiteranzahl!r}, "
            + f"bettenanzahl={self.bettenanzahl!r}, email={self.email!r})"
        )

    def set(self, krankenhaus: Self) -> None:
        """Setzen der Attribute, anhand eines anderen Krankenhaus-Objekts.

        param krankenhaus: Krankenhaus-Objekt mit den neuen Daten
        """
        self.name = krankenhaus.name
        self.mitarbeiteranzahl = krankenhaus.mitarbeiteranzahl
        self.bettenanzahl = krankenhaus.bettenanzahl
        self.email = krankenhaus.email
