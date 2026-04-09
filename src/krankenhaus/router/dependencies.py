"""Factory-Funktionen für Dependency Injection."""
from typing import Annotated

from fastapi import Depends

from krankenhaus.repository.krankenhaus_repository import KrankenhausRepository
from krankenhaus.service.krankenhaus_service import KrankenhausService
from krankenhaus.service.krankenhaus_write_service import KrankenhausWriteService

# from krankenhaus.service.krankenhaus_service import KrankenhausService


def get_repository() -> KrankenhausRepository:
    """Factory-Funktion für KrankenhausRepository.

    :return: Das Repository
    :rtype: KrankenhausRepository
    """
    return KrankenhausRepository()


def get_service(
    repo: Annotated[KrankenhausRepository, Depends(get_repository)],
) -> KrankenhausService:
    """Factory-Funktion für KrankenhausService."""
    return KrankenhausService(repo=repo)


def get_write_service(
    repo: Annotated[KrankenhausRepository, Depends(get_repository)],
) -> KrankenhausWriteService:
    """Factory-Funktion für KrankenhausWriteService."""
    return KrankenhausWriteService(repo=repo)
