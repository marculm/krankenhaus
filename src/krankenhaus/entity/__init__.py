"""__init__ für die Entity-Klassen."""

from krankenhaus.entity.adresse import Adresse
from krankenhaus.entity.base import Base
from krankenhaus.entity.fachbereich import Fachbereich
from krankenhaus.entity.krankenhaus import Krankenhaus

__all__ = ["Adresse", "Base", "Fachbereich", "Krankenhaus"]
