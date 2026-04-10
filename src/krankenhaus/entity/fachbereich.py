"""Entity-Klasse für die Fachbereiche."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from krankenhaus.entity.base import Base


class Fachbereich(Base):
    """Entity Klasse für die Fachbereiche eines Krankenhauses."""

    __tablename__ = "fachbereich"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )

    name: Mapped[str]
    """Der Name des Fachbereichs."""

    beschreibung: Mapped[str]
    """Die Beschreibung des Fachbereichs."""

    leitung: Mapped[str]
    """Die Leitung des Fachbereichs."""

    anzahlaerzte: Mapped[int]
    """Die Anzahl der Ärzte im Fachbereich."""

    krankenhaus_id: Mapped[int] = mapped_column(
        ForeignKey(column="krankenhaus.krankenhaus_id")
    )

    krankenhaus: Mapped[Krankenhaus] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="fachbereiche",
    )

    def __repr__(self) -> str:
        """Fachbereiche als String ausgeben."""
        return (
            f"Fachbereich(id={self.id}, name={self.name}, "
            + f"beschreibung={self.beschreibung}, leitung={self.leitung}, "
            + f"anzahlaerzte={self.anzahlaerzte})"
        )
