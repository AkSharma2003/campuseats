import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'service'))
import app as orders_app
import pytest

@pytest.fixture(autouse=True)
def reset_state():
    orders_app.orders.clear(); orders_app.idempotency.clear(); orders_app.rate_history.clear()

@pytest.fixture
def client():
    orders_app.app.config['TESTING'] = True
    return orders_app.app.test_client()

def valid_order(**extra):
    data = {'items':[{'id':'meal-1','qty':2}], 'address':'Hostel A'}
    data.update(extra); return data

def test_create_returns_201_location_and_json(client):
    r = client.post('/orders', json=valid_order())
    assert r.status_code == 201 and r.headers['Location'].startswith('/orders/')
    assert r.is_json and r.json['status'] == 'created'

def test_empty_cart_problem(client):
    r = client.post('/orders', json={'items':[], 'address':'Hostel A'})
    assert r.status_code == 422 and r.json['type'] == 'empty-cart'
    assert r.content_type.startswith('application/problem+json')

def test_collects_multiple_validation_errors(client):
    r = client.post('/orders', json={'items':[{'id':'meal-1','qty':0}], 'address':''})
    assert r.status_code == 422 and len(r.json['errors']) >= 2

def test_unknown_order(client):
    r = client.get('/orders/no-such-order')
    assert r.status_code == 404 and r.json['type'] == 'order-not-found'

def test_illegal_transition(client):
    r = client.post('/orders', json=valid_order()); oid = r.json['id']
    r = client.patch(f'/orders/{oid}', json={'status':'completed'})
    assert r.status_code == 409 and r.json['type'] == 'illegal-transition'

def test_idempotency(client):
    a = client.post('/orders', json=valid_order(), headers={'Idempotency-Key':'test-key'})
    b = client.post('/orders', json=valid_order(), headers={'Idempotency-Key':'test-key'})
    assert a.status_code == b.status_code == 201 and a.json['id'] == b.json['id']

def test_xml_negotiation(client):
    r = client.post('/orders', json=valid_order(), headers={'Accept':'application/xml'})
    assert r.status_code == 201 and r.content_type.startswith('application/xml')

def test_503_has_retry_after(client):
    r = client.post('/admin/simulate-unavailable')
    assert r.status_code == 503 and r.headers['Retry-After'] == '30'

def test_payment_declined(client):
    r = client.post('/orders', json=valid_order(payment_declined=True))
    assert r.status_code == 402 and r.json['type'] == 'payment-declined'

def test_delete_and_missing(client):
    r = client.post('/orders', json=valid_order()); oid = r.json['id']
    assert client.delete(f'/orders/{oid}').status_code == 204
    assert client.get(f'/orders/{oid}').status_code == 404
