"""Exceptions im Projekt Krankenhaus."""

from collections.abc import Mapping

__all__ = ["EmailExistsError", "NotFoundError", "VersionOutdatedError"]


class EmailExistsError(Exception):
    """Exception, falls die Emailadresse bereits existiert."""

    def __init__(self, email: str) -> None:
        """Initialisierung von EmailExistsError.

        :param email: Bereits existierende Emailadresse
        """
        super().__init__(f"Existierende Email: {email}")
        self.email = email


class NotFoundError(Exception):
    """Exception, falls kein Krankenhaus gefunden wurde."""

    def __init__(
        self,
        krankenhaus_id: int | None = None,
        suchparameter: Mapping[str, str] | None = None,
    ) -> None:
        """Initialisierung von NotFoundError mit ID und Suchparameter.

        :param krankenhaus_id: Krankenhaus-ID, zu der nichts gefunden wurde
        :param suchparameter: Suchparameter, zu denen nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.krankenhaus_id = krankenhaus_id
        self.suchparameter = suchparameter


class VersionOutdatedError(Exception):
    """Exception, falls die Version eines Krankenhauses veraltet ist."""

    def __init__(self, version: int) -> None:
        """Initialisierung von VersionOutdatedError.

        :param krankenhaus_id: ID des Krankenhauses mit veralteter Version
        :param version: Veraltete Version des Krankenhauses
        """
        super().__init__(f"Veraltete Version: {version}")
        self.version = version
