"""REST-Schnittstelle für Shutdown."""

import os
import signal
from typing import Any, Final

from fastapi import APIRouter, Depends
from loguru import logger

from krankenhaus.security.role import Role
from krankenhaus.security.roles_required import RolesRequired

__all__ = ["router"]


router: Final = APIRouter(tags=["Admin"])


# "Dependency Injection" durch Depends
@router.post("/shutdown", dependencies=[Depends(RolesRequired(Role.ADMIN))])
def shutdown() -> dict[str, Any]:
    """Der Server wird heruntergefahren."""
    logger.warning("Server shutting down without calling cleanup handlers.")
    # sys.exit(0)  # NOSONAR
    # os._exit(0)
    os.kill(os.getpid(), signal.SIGINT)  # NOSONAR
    return {"message": "Server is shutting down..."}
