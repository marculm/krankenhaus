"""CLI für das Projekt."""

from krankenhaus.asgi_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
