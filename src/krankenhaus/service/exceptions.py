"""Exceptions im Projekt Krankenhaus."""


class EmailExistsError(Exception):
    """Exception, falls die Emailadresse bereits existiert."""

    def __init__(self, email: str) -> None:
        """Initialisierung von EmailExistsError.

        :param email: Bereits existierende Emailadresse
        """
        super().__init__(f"Existierende Email: {email}")
        self.email = email
