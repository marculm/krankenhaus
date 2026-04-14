# ruff: noqa: S101
"""Tests für GET-Requests auf Namen."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
def test_get_namen() -> None:
    """Test für GET auf Namen mit vorhandenem Teilstring."""
    # arrange
    teil: Final = "Klinikum"
    erwartete_namen: Final = [
        "Fachklinikum",
        "Klinikum-Mitte",
        "Klinikum-Nord",
        "Klinikum-West",
        "Staedtisches-Klinikum",
    ]
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/namen/{teil}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, list)
    assert all(isinstance(name, str) for name in response_body)
    assert response_body == erwartete_namen


@mark.rest
@mark.get_request
def test_get_namen_not_found() -> None:
    """Test für GET auf Namen mit nicht vorhandenem Teilstring."""
    # arrange
    teil: Final = "NichtVorhandenXYZ"
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/namen/{teil}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
