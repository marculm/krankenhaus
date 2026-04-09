"""Pydantic-Model für die Adresse."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from krankenhaus.entity import Adresse

__all__ = ["AdresseModel"]


class AdresseModel(BaseModel):
    """Pydantic-Model für die Adresse."""

    plz: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    """Postleitzahl"""
    ort: Annotated[str, StringConstraints(max_length=64)]
    """Ort"""
    strasse: str
    """Straße"""
    hausnummer: str
    """Hausnummer"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "plz": "99999",
                "ort": "Testort",
                "strasse": "Teststraße",
                "hausnummer": "1a",
            },
        }
    )

    def to_adresse(self) -> Adresse:
        """Konvertierung in ein Adresse-Objekt für SQLAlchemy.

        :return: Adresse-Objekt für SQLAlchemy
        :rtype: Adresse
        """
        adresse_dict = self.model_dump()
        adresse_dict["id"] = None
        adresse_dict["krankenhaus_id"] = None
        adresse_dict["krankenhaus"] = None

        return Adresse(**adresse_dict)
