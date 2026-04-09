"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from krankenhaus.router.adressse_model import AdresseModel
from krankenhaus.router.fachbereich_model import FachbereichModel
from krankenhaus.router.health_router import liveness, readiness
from krankenhaus.router.health_router import router as health_router
from krankenhaus.router.krankenhaus_model import KrankenhausModel
from krankenhaus.router.krankenhaus_router import (
    get,
    get_by_id,
    get_namen,
    krankenhaus_router,
)
from krankenhaus.router.krankenhaus_update_model import KrankenhausUpdateModel
from krankenhaus.router.krankenhaus_write_router import (
    krankenhaus_write_router,
)

# from krankenhaus.router.krankenhaus_write_router import (
#     delete_by_id,
#     krankenhaus_write_router,
#     post,
#     put,
# )
from krankenhaus.router.shutdown_router import router as shutdown_router
from krankenhaus.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "AdresseModel",
    "FachbereichModel",
    "KrankenhausModel",
    "KrankenhausUpdateModel",
    # "delete_by_id",
    "get",
    "get_by_id",
    "get_namen",
    "health_router",
    "krankenhaus_router",
    "krankenhaus_write_router",
    "liveness",
    # "post",
    # "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
