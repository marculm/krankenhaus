"""Pydantic Models für das Updaten eines Krankenhaus."""

from typing import Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, EmailStr

from krankenhaus.entity import Krankenhaus

__all__: list[str] = ["KrankenhausUpdateModel"]


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
        krankenhaus_dict["fachbereiche"] = []
        krankenhaus_dict["erzeugt"] = None
        krankenhaus_dict["aktualisiert"] = None

        return krankenhaus_dict

    def to_krankenhaus(self) -> Krankenhaus:
        """Konvertiert das Pydantic Model in ein Krankenhaus Objekt.

        :return: Krankenhaus-Objekt für SQLAlchemy
        :rtype: Krankenhaus
        """
        logger.debug("self={}", self)
        krankenhaus_dict = self.to_dict()

        krankenhaus = Krankenhaus(**krankenhaus_dict)
        logger.debug("krankenhaus={}", krankenhaus)
        return krankenhaus
