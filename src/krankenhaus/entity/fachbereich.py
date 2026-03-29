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

    beschreibung: Mapped[str]

    leitung: Mapped[str]

    anzahlaerzte: Mapped[int]

    krankenhausid: Mapped[int] = mapped_column(
        ForeignKey(column="krankenhaus.krankenhausid")
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
