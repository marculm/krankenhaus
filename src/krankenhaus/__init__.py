"""Modul Deklaration."""

from krankenhaus.asgi_server import run
from krankenhaus.fastapi_app import app

__all__ = ["app", "main"]


def main():  # noqa: RUF067
    """main-Funktion, damit das Modul als Skript aufgerufen werden kann."""
    run()
