# ruff: noqa: D103, S101
"""Tests für PUT-Requests."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

EMAIL_UPDATE: Final = "put@test.de"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    krankenhaus_id: Final = 10
    if_match: Final = '"0"'
    geaendertes_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": EMAIL_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}", "If-Match": if_match}

    # act
    response: Final = put(
        f"{rest_url}/{krankenhaus_id}",
        json=geaendertes_krankenhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    krankenhaus_id: Final = 00
    if_match: Final = '"0"'
    geaendertes_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": EMAIL_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}", "If-Match": if_match}

    # act
    response: Final = put(
        f"{rest_url}/{krankenhaus_id}",
        json=geaendertes_krankenhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_ohne_version() -> None:
    # arrange
    krankenhaus_id: Final = 10
    geaendertes_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": EMAIL_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{krankenhaus_id}",
        json=geaendertes_krankenhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_version() -> None:
    # arrange
    krankenhaus_id: Final = 10
    if_match: Final = '"-1"'
    geaendertes_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": EMAIL_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}", "If-Match": if_match}

    # act
    response: Final = put(
        f"{rest_url}/{krankenhaus_id}",
        json=geaendertes_krankenhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
