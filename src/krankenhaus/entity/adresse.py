"""Entity-Klasse der Adresse."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from krankenhaus.entity.base import Base


class Adresse(Base):
    """Entity-Klasse der Adresse."""

    __tablename__ = "adresse"

    id: Mapped[int] = mapped_column(Identity(start=1000), primary_key=True)

    strasse: Mapped[str]

    hausnummer: Mapped[str]

    plz: Mapped[str]

    ort: Mapped[str]

    krankenhaus_id: Mapped[int] = mapped_column(ForeignKey("krankenhaus.id"))

    krankenhaus: Mapped[Krankenhaus] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="adresse"
    )

    def __repr__(self) -> str:
        """Adresse als String ausgeben."""
        return (
            f"Adresse(id={self.id}, "
            + f"strasse={self.strasse}, "
            + f"hausnummer={self.hausnummer}, "
            + f"plz={self.plz}, "
            + f"ort={self.ort})"
        )
