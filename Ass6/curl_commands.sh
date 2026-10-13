#!/usr/bin/env bash
# Run while Ass6/service/app.py is running at http://127.0.0.1:5000
set -u
BASE="${BASE_URL:-http://127.0.0.1:5000}"
echo '=== Successful order creation (save returned ID and Location) ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Idempotency-Key: demo-order-001' -d '{"items":[{"id":"meal-1","qty":2}],"address":"Hostel A"}'
echo; echo '=== Empty cart (422 / empty-cart) ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -d '{"items":[],"address":"Hostel A"}'
echo; echo '=== Two field validation errors (422) ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -d '{"items":[{"id":"meal-1","qty":0}],"address":""}'
echo; echo '=== Unknown order (404) ==='
curl -i "$BASE/orders/no-such-order"
echo; echo '=== Item unavailable (409) ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -d '{"items":[{"id":"meal-1","qty":1,"available":false}],"address":"Hostel A"}'
echo; echo '=== Payment declined demonstration (402) ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -d '{"items":[{"id":"meal-1","qty":1}],"address":"Hostel A","payment_declined":true}'
echo; echo '=== XML negotiation ==='
curl -i -X POST "$BASE/orders" -H 'Content-Type: application/json' -H 'Accept: application/xml' -d '{"items":[{"id":"meal-1","qty":1}],"address":"Hostel A"}'
echo; echo '=== 503 transient failure / Retry-After ==='
curl -i -X POST "$BASE/admin/simulate-unavailable"
echo; echo '=== Rate limit ==='
for i in $(seq 1 25); do curl -s -o /dev/null -w '%{http_code}\n' "$BASE/health"; done
