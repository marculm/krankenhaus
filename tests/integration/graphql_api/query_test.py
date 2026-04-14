# ruff: noqa: S101, D103
"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login
from httpx import post
from pytest import mark


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                krankenhaus(krankenhausId: "999999") {
                    id
                    name
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["krankenhaus"] is None
    assert response_body.get("errors") is None
