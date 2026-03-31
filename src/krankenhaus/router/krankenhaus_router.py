"""Krankenhaus Router für Get-Requests."""

from typing import Final

from fastapi import APIRouter

__all__ = ["krankenhaus_router"]

krankenhaus_router: Final = APIRouter(tags=["Lesen"])


@krankenhaus_router.get("/helloworld")
def helloworld() -> dict[str, str]:
    """Router Test."""
    return {"msg": "Hello World!"}
