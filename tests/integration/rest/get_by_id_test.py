# ruff: noqa: S101
"""Tests für GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


# in pyproject.toml bei der Table [tool.pytest.ini_options] gibt es das Array "markers"
@mark.rest
@mark.get_request
@mark.parametrize("krankenhaus_id", [10, 20, 30])
def test_get_by_id(krankenhaus_id: int) -> None:
    """Test für GET mit Query-Parameter, wenn der Nutzer ein Admin ist."""
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{krankenhaus_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == krankenhaus_id


@mark.rest
@mark.get_request
def test_get_by_id_not_found() -> None:
    """Test für GET mit nicht vorhandener ID."""
    # arrange
    krankenhaus_id: Final = 999
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{krankenhaus_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
