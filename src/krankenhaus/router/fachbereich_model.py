"""Pydantic-Model für die Fachbereiche."""

from pydantic import BaseModel, ConfigDict

from krankenhaus.entity.fachbereich import Fachbereich

__all__: list[str] = ["FachbereichModel"]


class FachbereichModel(BaseModel):
    """Pydantic-Model für die Fachbereiche."""

    name: str
    """Der Name des Fachbereichs."""

    beschreibung: str
    """Die Beschreibung des Fachbereichs."""

    leitung: str
    """Die Leitung des Fachbereichs."""

    anzahlaerzte: int
    """Die Anzahl der Ärzte im Fachbereich."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Kardiologie",
                "beschreibung": "Beschäftigt sich mit Erkrankungen des Herzens.",
                "leitung": "Dr. med. Max Mustermann",
                "anzahlaerzte": 10,
            }
        }
    )

    def to_fachbereich(self) -> Fachbereich:
        """Konvertiert das Pydantic-Model in ein Fachbereich-Entity-Objekt.

        :return: Fachbereich-Objekt für SQLAlchemy
        :rtype: Fachbereich
        """
        fachbereich_dict = self.model_dump()
        fachbereich_dict["id"] = None
        fachbereich_dict["krankenhausid"] = None
        fachbereich_dict["krankenhaus"] = None

        return Fachbereich(**fachbereich_dict)
