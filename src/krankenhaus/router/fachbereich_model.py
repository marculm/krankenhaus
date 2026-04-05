"""Pydantic-Model für die Fachbereiche."""

from pydantic import BaseModel, ConfigDict

from krankenhaus.entity.fachbereich import Fachbereich

__all__: list[str] = ["FachbereichModel"]


class FachbereichModel(BaseModel):
    """Pydantic-Model für die Fachbereiche."""

    name: str
    beschreibung: str
    leitung: str
    anzahlaerzte: int

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
        """Konvertiert das Pydantic-Model in ein Fachbereich-Entity-Objekt."""
        fachbereich_dict = self.model_dump()
        fachbereich_dict["id"]
        fachbereich_dict["krankenhausid"]
        fachbereich_dict["krankenhaus"]

        return Fachbereich(**fachbereich_dict)
