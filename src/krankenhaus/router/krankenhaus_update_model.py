"""Pydantic Models für das Updaten eines Krankenhaus."""

from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr


class KrankenhausUpdateModel(BaseModel):
    """Pydantic Model für das Update eines Krankenhauses."""

    name: str
    """Der Name des Krankenhauses."""

    mitarbeiteranzahl: int
    """Die Anzahl der Mitarbeiter im Krankenhaus."""

    bettenanzahl: int
    """Die Anzahl der Betten im Krankenhaus."""

    email: EmailStr
    """Die einduetige E-Mail-Adresse des Krankenhauses."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nachname": "Test",
                "mitarbeiteranzahl": 50,
                "bettenanzahl": 100,
                "email": "test@acme.com",
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertiert das Pydantic Model in ein Dictionary.

        :return: Dictionary mit den Attributen des Pydantic Models
        :rtype: dict[str, Any]
        """
        krankenhaus_dict = self.model_dump()
        krankenhaus_dict["id"] = None
        krankenhaus_dict["adresse"] = None
        krankenhaus_dict["fachbereich"] = []
        krankenhaus_dict["erzeugt"] = None
        krankenhaus_dict["aktualisiert"] = None

        return krankenhaus_dict
