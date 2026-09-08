import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import app as application

@pytest.fixture
def client():
    return application.app.test_client()

BODY = {"restaurantId": 10, "name": "Burger", "pricePaise": 15000}

def test_create_succeeds(client):
    r = client.post("/items", json=BODY)
    assert r.status_code == 201
    assert "Location" in r.headers

def test_idempotent_repeat(client):
    h = {"Idempotency-Key": "k-100"}
    a = client.post("/items", json=BODY, headers=h)
    b = client.post("/items", json=BODY, headers=h)
    assert (a.status_code, b.status_code) == (201, 200)
    assert a.json["id"] == b.json["id"]

def test_bad_body_returns_400(client):
    r = client.post("/items", json={"name": ""})
    assert r.status_code == 400

def test_unknown_id_404(client):
    assert client.get("/items/999").status_code == 404