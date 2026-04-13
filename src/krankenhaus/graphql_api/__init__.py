"""Modul für die GraphQL-Schnittstelle."""

from krankenhaus.graphql_api.graphql_types import Suchparameter
from krankenhaus.graphql_api.schema import Query, get_context, graphql_router, schema

__all__ = [
    "Query",
    "Suchparameter",
    "get_context",
    "graphql_router",
    "schema",
]
