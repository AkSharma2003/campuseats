import sys
from pathlib import Path

# Ass5/service ko Python import path mein add karta hai
SERVICE_DIR = Path(__file__).resolve().parents[1] / "service"
sys.path.insert(0, str(SERVICE_DIR))

from app import app


def test_create_item():
    client = app.test_client()

    response = client.post(
        "/items",
        headers={
            "Authorization": "Bearer test-token",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Idempotency-Key": "pytest-create-001",
        },
        json={
            "restaurantId": 1,
            "name": "Pytest Burger",
            "pricePaise": 5000,
        },
    )

    assert response.status_code == 201
    assert "Location" in response.headers


def test_get_missing_item():
    client = app.test_client()

    response = client.get(
        "/items/999999",
        headers={
            "Accept": "application/json",
        },
    )

    assert response.status_code == 404


def test_conditional_get_returns_304():
    client = app.test_client()

    create_response = client.post(
        "/items",
        headers={
            "Authorization": "Bearer test-token",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Idempotency-Key": "pytest-etag-001",
        },
        json={
            "restaurantId": 1,
            "name": "Pytest ETag Item",
            "pricePaise": 6000,
        },
    )

    assert create_response.status_code == 201

    item_url = create_response.headers["Location"]

    get_response = client.get(
        item_url,
        headers={
            "Accept": "application/json",
        },
    )

    assert get_response.status_code == 200
    assert "ETag" in get_response.headers

    etag = get_response.headers["ETag"]

    conditional_response = client.get(
        item_url,
        headers={
            "Accept": "application/json",
            "If-None-Match": etag,
        },
    )

    assert conditional_response.status_code == 304
    assert conditional_response.get_data() == b""


def test_wrong_if_match_returns_412():
    client = app.test_client()

    create_response = client.post(
        "/items",
        headers={
            "Authorization": "Bearer test-token",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Idempotency-Key": "pytest-ifmatch-001",
        },
        json={
            "restaurantId": 1,
            "name": "Pytest IfMatch Item",
            "pricePaise": 7000,
        },
    )

    assert create_response.status_code == 201

    item_url = create_response.headers["Location"]

    response = client.post(
        f"{item_url}/availability",
        headers={
            "Authorization": "Bearer test-token",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "If-Match": '"wrong-etag"',
        },
        json={
            "isAvailable": False,
        },
    )

    assert response.status_code == 412


def test_missing_auth_returns_401():
    client = app.test_client()

    response = client.post(
        "/items",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Idempotency-Key": "pytest-auth-001",
        },
        json={
            "restaurantId": 1,
            "name": "Unauthorized Item",
            "pricePaise": 5000,
        },
    )

    assert response.status_code == 401