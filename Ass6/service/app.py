"""CS543 Assignment 6 - Orders service (standalone, in-memory teaching implementation)."""
from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import HTTPException
from collections import defaultdict, deque
from datetime import datetime, timezone
import threading, uuid, json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
orders = {}
idempotency = {}
rate_history = defaultdict(deque)
lock = threading.Lock()
RATE_LIMIT = 20
RATE_WINDOW_SECONDS = 60

ERROR_TYPES = {
    'empty-cart': ('Empty Cart', 422),
    'item-unavailable': ('Item Unavailable', 409),
    'payment-declined': ('Payment Declined', 402),
    'order-not-found': ('Order Not Found', 404),
    'illegal-transition': ('Illegal Order Transition', 409),
    'validation-error': ('Validation Failed', 422),
    'not-acceptable': ('Not Acceptable', 406),
    'unsupported-media-type': ('Unsupported Media Type', 415),
    'rate-limit-exceeded': ('Too Many Requests', 429),
    'internal-error': ('Internal Server Error', 500),
    'method-not-allowed': ('Method Not Allowed', 405),
    'not-found': ('Not Found', 404),
}

def problem(status, type_name, detail, errors=None, retry_after=None):
    title = ERROR_TYPES.get(type_name, ('Request Failed', status))[0]
    body = {'type': type_name, 'title': title, 'status': status, 'detail': detail}
    if errors is not None:
        body['errors'] = errors
    response = jsonify(body)
    response.status_code = status
    response.headers['Content-Type'] = 'application/problem+json; charset=utf-8'
    if retry_after is not None:
        response.headers['Retry-After'] = str(retry_after)
    return response

@app.after_request
def set_headers(response):
    if response.get_data() and 'Content-Type' not in response.headers:
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    elif response.get_data() and 'charset=' not in response.headers.get('Content-Type','').lower():
        response.headers['Content-Type'] = response.headers['Content-Type'].split(';')[0] + '; charset=utf-8'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.before_request
def rate_limit():
    # Keep rate limiting deterministic for a given client. This demo limit is intentionally high.
    now = datetime.now(timezone.utc).timestamp()
    q = rate_history[request.remote_addr or 'local']
    while q and now - q[0] > RATE_WINDOW_SECONDS:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return problem(429, 'rate-limit-exceeded', 'Request limit reached; retry later.', retry_after=60)
    q.append(now)

@app.errorhandler(HTTPException)
def http_error(exc):
    status = exc.code or 500
    typ = 'not-found' if status == 404 else 'method-not-allowed' if status == 405 else 'internal-error'
    return problem(status, typ, 'The requested operation could not be completed.')

@app.errorhandler(Exception)
def unexpected_error(exc):
    app.logger.exception('Unhandled internal error')
    return problem(500, 'internal-error', 'An unexpected server error occurred.')

def wants_xml():
    accept = request.headers.get('Accept', '')
    if not accept or '*/*' in accept or 'application/json' in accept:
        return False, None
    if 'application/xml' in accept or 'text/xml' in accept:
        return True, None
    return False, problem(406, 'not-acceptable', 'Supported response formats are application/json and application/xml.')

def represent(data, xml=False, status=200, location=None):
    if xml:
        # Small, predictable XML serializer for this assignment's simple object/list structure.
        def esc(v):
            return str(v).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
        def node(k, v):
            if isinstance(v, dict):
                inner = ''.join(node(str(kk), vv) for kk, vv in v.items())
                return f'<{k}>{inner}</{k}>'
            if isinstance(v, list):
                return ''.join(node(k[:-1] if k.endswith('s') else 'item', x) for x in v)
            return f'<{k}>{esc(v)}</{k}>'
        body = '<?xml version="1.0" encoding="UTF-8"?>' + node('response', data)
        r = Response(body, status=status, content_type='application/xml; charset=utf-8')
    else:
        r = jsonify(data); r.status_code = status
    if location:
        r.headers['Location'] = location
    return r

def validate_order(payload):
    errors = []
    if not isinstance(payload, dict):
        return [{'field': '$', 'message': 'Request body must be a JSON object.'}]
    items = payload.get('items')
    if not isinstance(items, list) or len(items) == 0:
        errors.append({'field': 'items', 'message': 'Items must be a non-empty array.'})
    elif isinstance(items, list):
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append({'field': f'items[{i}]', 'message': 'Each item must be an object.'}); continue
            qty = item.get('qty')
            if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
                errors.append({'field': f'items[{i}].qty', 'message': 'Quantity must be an integer greater than or equal to 1.'})
            if not item.get('id'):
                errors.append({'field': f'items[{i}].id', 'message': 'Item id is required.'})
            if item.get('available') is False:
                errors.append({'field': f'items[{i}].id', 'message': 'Item is unavailable.'})
    if not isinstance(payload.get('address'), str) or not payload.get('address','').strip():
        errors.append({'field': 'address', 'message': 'Address is required.'})
    return errors

def get_body():
    if not request.is_json:
        return None, problem(415, 'unsupported-media-type', 'Send the request body as application/json.')
    try:
        return request.get_json(silent=False), None
    except Exception:
        return None, problem(400, 'validation-error', 'Request body is not valid JSON.', errors=[{'field':'$','message':'Malformed JSON.'}])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok'})

@app.route('/orders', methods=['GET'])
def list_orders():
    xml, err = wants_xml()
    if err: return err
    return represent({'orders': list(orders.values())}, xml)

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    xml, err = wants_xml()
    if err: return err
    order = orders.get(order_id)
    if not order: return problem(404, 'order-not-found', f'No order exists with id {order_id}.')
    return represent(order, xml)

@app.route('/orders', methods=['POST'])
def create_order():
    xml, err = wants_xml()
    if err: return err
    payload, err = get_body()
    if err: return err
    errors = validate_order(payload)
    if errors:
        if any(e['field'] == 'items' and 'non-empty' in e['message'] for e in errors):
            return problem(422, 'empty-cart', 'An order must contain at least one item.', errors=errors)
        if any('unavailable' in e['message'].lower() for e in errors):
            return problem(409, 'item-unavailable', 'One or more requested items are unavailable.', errors=errors)
        return problem(422, 'validation-error', 'The order contains invalid fields.', errors=errors)
    if payload.get('payment_declined') is True:
        return problem(402, 'payment-declined', 'The payment provider declined this payment.')
    key = request.headers.get('Idempotency-Key')
    if key and key in idempotency:
        oid = idempotency[key]
        return represent(orders[oid], xml, 201, f'/orders/{oid}')
    with lock:
        oid = str(uuid.uuid4())
        order = {'id': oid, 'items': payload['items'], 'address': payload['address'], 'status': 'created', 'createdAt': datetime.now(timezone.utc).isoformat()}
        orders[oid] = order
        if key: idempotency[key] = oid
    return represent(order, xml, 201, f'/orders/{oid}')

@app.route('/orders/<order_id>', methods=['PATCH'])
def update_order(order_id):
    xml, err = wants_xml()
    if err: return err
    if order_id not in orders: return problem(404, 'order-not-found', f'No order exists with id {order_id}.')
    payload, err = get_body()
    if err: return err
    if not isinstance(payload, dict) or not isinstance(payload.get('status'), str):
        return problem(422, 'validation-error', 'A status field is required.', errors=[{'field':'status','message':'Status must be a string.'}])
    current = orders[order_id]['status']; target = payload['status']
    allowed = {'created': {'confirmed','cancelled'}, 'confirmed': {'preparing','cancelled'}, 'preparing': {'ready'}, 'ready': {'completed'}}
    if target not in allowed.get(current, set()):
        return problem(409, 'illegal-transition', f'Cannot change order status from {current} to {target}.')
    orders[order_id]['status'] = target
    return represent(orders[order_id], xml)

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    if order_id not in orders: return problem(404, 'order-not-found', f'No order exists with id {order_id}.')
    if orders[order_id]['status'] not in ('created','cancelled'):
        return problem(409, 'illegal-transition', 'Only created or cancelled orders may be deleted.')
    del orders[order_id]
    return Response(status=204)

@app.route('/admin/simulate-unavailable', methods=['POST'])
def simulate_unavailable():
    """Testing hook: returns a transient 503 response with Retry-After."""
    return problem(503, 'internal-error', 'Service temporarily unavailable; retry later.', retry_after=30)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(__import__('os').environ.get('PORT','5000')), debug=False)
