# ruff: noqa: D103, S101
"""Tests für POST-Requests."""
from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neues_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": "krankenhaus@test.de",
        "adresse": {
            "strasse": "Teststrasse",
            "hausnummer": "1",
            "plz": "12345",
            "ort": "Teststadt"
        },
        "fachbereiche": [
            {
                "name": "test",
                "beschreibung": "Testbereich",
                "leitung": "Dr. Test",
                "anzahlaerzte": 100
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_krankenhaus,
        headers=headers,
        verify=ctx
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neues_krankenhaus: Final = {
        "name": "Kein Krankenhaus",
        "mitarbeiteranzahl": "test",
        "bettenanzahl": 200,
        "email": "krankenhaus",
        "adresse": {
            "strasse": "Teststrasse",
            "hausnummer": "1",
            "plz": "123",
            "ort": "Teststadt"
        },
        "fachbereiche": [
            {
                "name": "test",
                "beschreibung": "Testbereich",
                "leitung": "Dr. Test",
                "anzahlaerzte": 100
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_krankenhaus,
        headers=headers,
        verify=ctx
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "mitarbeiteranzahl" in body
    assert "email" in body
    assert "plz" in body


@mark.rest
@mark.post_request
def test_post_email_exist() -> None:
    # arrange
    email_exists: Final = "vinzentius@krankenhaus.de"
    neues_krankenhaus: Final = {
        "name": "Testkrankenhaus",
        "mitarbeiteranzahl": 100,
        "bettenanzahl": 200,
        "email": email_exists,
        "adresse": {
            "strasse": "Teststrasse",
            "hausnummer": "1",
            "plz": "12345",
            "ort": "Teststadt"
        },
        "fachbereiche": [
            {
                "name": "test",
                "beschreibung": "Testbereich",
                "leitung": "Dr. Test",
                "anzahlaerzte": 100
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neues_krankenhaus,
        headers=headers,
        verify=ctx
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert email_exists in response.text
