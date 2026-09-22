import os
import time
import random
import uuid
import hashlib
from collections import defaultdict

import requests

from flask import Flask, request, jsonify

import store
from errors import problem


app = Flask(__name__)


# ============================================================
# B5 - PER-CLIENT RATE LIMITING
# ============================================================

RATE_LIMIT = 5
RATE_WINDOW = 60

# Stores request timestamps separately for each client.
rate_limits = defaultdict(list)


# ============================================================
# B6 - CORS
# ============================================================

@app.after_request
def add_cors_headers(response):

    # Allow requests from any origin.
    response.headers["Access-Control-Allow-Origin"] = "*"

    # HTTP methods allowed by the API.
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, OPTIONS"
    )

    # Request headers allowed by the API.
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization, Accept, "
        "Idempotency-Key, If-None-Match, If-Match"
    )

    # B7 - Security header
    response.headers["X-Content-Type-Options"] = "nosniff"

    # B7 - HSTS header
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    return response


# ============================================================
# B1 - CONTENT NEGOTIATION
# ============================================================

def check_accept():

    """
    Only application/json responses are supported.
    Unsupported Accept header -> 406.
    """

    accept = request.headers.get("Accept")

    # No Accept header -> allow request.
    if not accept:
        return None

    # JSON is supported.
    if "application/json" in accept:
        return None

    # */* means client accepts any response format.
    if "*/*" in accept:
        return None

    # Unsupported response format.
    return problem(
        406,
        "not-acceptable",
        detail="Only application/json responses are supported"
    )


# ============================================================
# B3 - AUTHORIZATION
# ============================================================

def check_authorization():

    """
    Protected endpoints require:

    Authorization: Bearer <token>
    """

    auth = request.headers.get("Authorization")

    # Missing or invalid Authorization header.
    if not auth or not auth.startswith("Bearer "):

        return problem(
            401,
            "unauthorized",
            detail="Missing or invalid Bearer token"
        )

    # Extract token.
    token = auth[7:].strip()

    # Empty token.
    if not token:

        return problem(
            401,
            "unauthorized",
            detail="Missing or empty Bearer token"
        )

    return None


# ============================================================
# B4 - ETAG
# ============================================================

def generate_etag(item):

    """
    Generate an ETag from the current item representation.
    """

    data = str(
        item.as_json()
    ).encode("utf-8")

    return '"' + hashlib.sha256(data).hexdigest() + '"'


# ============================================================
# B5 - RATE LIMIT CHECK
# ============================================================

def check_rate_limit():

    # Identify client by IP address.
    client_id = request.remote_addr or "unknown"

    now = time.time()

    timestamps = rate_limits[client_id]

    # Remove requests older than 60 seconds.
    rate_limits[client_id] = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < RATE_WINDOW
    ]

    timestamps = rate_limits[client_id]

    # Rate limit exceeded.
    if len(timestamps) >= RATE_LIMIT:

        response, status = problem(
            429,
            "rate-limit-exceeded",
            detail="Rate limit exceeded"
        )

        response.headers["X-RateLimit-Limit"] = str(
            RATE_LIMIT
        )

        response.headers["X-RateLimit-Remaining"] = "0"

        retry_after = max(
            1,
            int(
                RATE_WINDOW
                - (now - timestamps[0])
            )
        )

        response.headers["Retry-After"] = str(
            retry_after
        )

        return (response, status), None

    # Record current request.
    timestamps.append(now)

    remaining = RATE_LIMIT - len(timestamps)

    return None, {
        "X-RateLimit-Limit": str(RATE_LIMIT),
        "X-RateLimit-Remaining": str(remaining)
    }


# ============================================================
# D - EXTERNAL HTTP RETRY
# ============================================================

PAYMENTS_URL = os.environ.get(
    "PAYMENTS_URL",
    "http://localhost:8080"
)


def notify_external_sync_with_retry(item_id: int):

    """
    External HTTP call with:

    - timeout
    - maximum 3 attempts
    - exponential backoff
    - jitter
    - Idempotency-Key
    - no retry for 4xx errors
    """

    key = str(uuid.uuid4())

    for attempt in range(3):

        try:

            response = requests.post(
                f"{PAYMENTS_URL}/payments",

                json={
                    "orderId": item_id,
                    "cardToken": "tok_sync",
                    "amount": 100,
                    "currency": "INR"
                },

                headers={
                    "Idempotency-Key": key
                },

                timeout=2.0
            )

            # Successful request.
            if response.status_code in (200, 201):

                return response.json()

            # Do not retry 4xx client errors.
            if 400 <= response.status_code < 500:

                raise Exception(
                    "Client error (4xx) - DO NOT RETRY"
                )

        except Exception as e:

            if (
                attempt == 2
                or "DO NOT RETRY" in str(e)
            ):
                break

            # Exponential backoff + random jitter.
            wait_time = (
                (2 ** attempt)
                + random.uniform(0, 0.5)
            )

            time.sleep(wait_time)


# ============================================================
# VALIDATION
# ============================================================

def validate(body: dict) -> list:

    errors = []

    # restaurantId
    if not isinstance(
        body.get("restaurantId"),
        int
    ):

        errors.append([
            "restaurantId",
            "must be integer"
        ])

    # name
    if (
        not body.get("name")
        or not isinstance(
            body.get("name"),
            str
        )
    ):

        errors.append([
            "name",
            "required string"
        ])

    # pricePaise
    price = body.get("pricePaise")

    if (
        not isinstance(price, int)
        or price <= 0
    ):

        errors.append([
            "pricePaise",
            "positive integer required"
        ])

    return errors


# ============================================================
# POST /items
# CREATE MENU ITEM
# ============================================================

@app.post("/items")
def create_item():

    # --------------------------------------------------------
    # B5 - Rate limit
    # --------------------------------------------------------

    rate_result = check_rate_limit()

    # Rate limit exceeded.
    if rate_result[1] is None:

        return rate_result[0]

    rate_headers = rate_result[1]

    # --------------------------------------------------------
    # B3 - Authorization
    # --------------------------------------------------------

    auth_error = check_authorization()

    if auth_error:

        return auth_error

    # --------------------------------------------------------
    # B1 - Accept
    # --------------------------------------------------------

    accept_error = check_accept()

    if accept_error:

        return accept_error

    # --------------------------------------------------------
    # Read JSON body
    # --------------------------------------------------------

    body = request.get_json(
        silent=True
    )

    if body is None:

        return problem(
            400,
            "invalid-request",
            detail="Malformed JSON request"
        )

    # --------------------------------------------------------
    # Validate body
    # --------------------------------------------------------

    errors = validate(body)

    if errors:

        return problem(
            400,
            "invalid-request",
            errors=errors
        )

    # --------------------------------------------------------
    # B2 - Domain refusal
    # --------------------------------------------------------

    if body.get("name") == "BAD_ITEM":

        return problem(
            422,
            "domain-refusal",
            detail="Item domain policy failure"
        )

    # --------------------------------------------------------
    # C3 - Idempotency-Key
    # --------------------------------------------------------

    key = request.headers.get(
        "Idempotency-Key"
    )

    if key:

        # Existing key in store.
        prior = store.find_by_key(key)

        if prior:

            response = jsonify(
                prior.as_json()
            )

            # Return original successful result.
            response.status_code = 201

            response.headers["Location"] = (
                f"/items/{prior.id}"
            )

            for header, value in rate_headers.items():

                response.headers[header] = value

            return response

    # --------------------------------------------------------
    # Create new item
    # --------------------------------------------------------

    item = store.create(
        body["restaurantId"],
        body["name"],
        body["pricePaise"],
        key
    )

    response = jsonify(
        item.as_json()
    )

    # B2 - Created
    response.status_code = 201

    # B2 - Location
    response.headers["Location"] = (
        f"/items/{item.id}"
    )

    # B5 - Rate-limit headers
    for header, value in rate_headers.items():

        response.headers[header] = value

    return response


# ============================================================
# GET /items/{id}
# SINGLE ITEM
# ============================================================

@app.route(
    "/items/<int:item_id>",
    methods=["GET"],
    provide_automatic_options=False
)
def get_item(item_id: int):

    # --------------------------------------------------------
    # B1 - Content negotiation
    # --------------------------------------------------------

    accept_error = check_accept()

    if accept_error:

        return accept_error

    # --------------------------------------------------------
    # Find item
    # --------------------------------------------------------

    item = store.find(item_id)

    if not item:

        return problem(
            404,
            "item-not-found",
            detail=f"Item {item_id} not found"
        )

    # --------------------------------------------------------
    # B4 - Generate ETag
    # --------------------------------------------------------

    etag = generate_etag(item)

    # --------------------------------------------------------
    # C1 - If-None-Match
    # --------------------------------------------------------

    client_etag = request.headers.get(
        "If-None-Match"
    )

    if (
        client_etag
        and client_etag == etag
    ):

        # 304 response MUST NOT contain a body.
        response = app.response_class(
            status=304
        )

        response.headers["ETag"] = etag

        response.headers["Cache-Control"] = (
            "private, max-age=60"
        )

        return response

    # --------------------------------------------------------
    # Normal 200 response
    # --------------------------------------------------------

    response = jsonify(
        item.as_json()
    )

    response.status_code = 200

    response.headers["ETag"] = etag

    response.headers["Cache-Control"] = (
        "private, max-age=60"
    )

    return response


# ============================================================
# GET /items
# LIST MENU ITEMS
# ============================================================

@app.get("/items")
def list_items():

    # --------------------------------------------------------
    # B1 - Accept
    # --------------------------------------------------------

    accept_error = check_accept()

    if accept_error:

        return accept_error

    # --------------------------------------------------------
    # A4 - Filtering
    # --------------------------------------------------------

    restaurant_id = request.args.get(
        "restaurantId",
        type=int
    )

    # Current store implementation requires
    # restaurantId for listing.
    if restaurant_id is None:

        return problem(
            400,
            "invalid-request",
            detail="Missing restaurantId"
        )

    items = store.find_by_restaurant(
        restaurant_id
    )

    # --------------------------------------------------------
    # Convert items to JSON
    # --------------------------------------------------------

    items = [
        item.as_json()
        for item in items
    ]

    # --------------------------------------------------------
    # A4 - Sorting
    # --------------------------------------------------------

    sort_field = request.args.get(
        "sort",
        "createdAt"
    )

    sort_order = request.args.get(
        "order",
        "asc"
    )

    allowed_sort_fields = {
        "name",
        "pricePaise",
        "createdAt"
    }

    if sort_field not in allowed_sort_fields:

        return problem(
            400,
            "invalid-request",
            detail="Invalid sort field"
        )

    if sort_order not in (
        "asc",
        "desc"
    ):

        return problem(
            400,
            "invalid-request",
            detail="order must be asc or desc"
        )

    # Sort.
    items.sort(
        key=lambda item:
            item.get(sort_field, ""),
        reverse=(
            sort_order == "desc"
        )
    )

    # --------------------------------------------------------
    # A4 - Pagination
    # --------------------------------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )

    limit = request.args.get(
        "limit",
        20,
        type=int
    )

    if page < 1:

        return problem(
            400,
            "invalid-request",
            detail="page must be >= 1"
        )

    if (
        limit < 1
        or limit > 100
    ):

        return problem(
            400,
            "invalid-request",
            detail="limit must be between 1 and 100"
        )

    start = (
        page - 1
    ) * limit

    end = start + limit

    items = items[start:end]

    return jsonify(items), 200


# ============================================================
# POST /items/{id}/availability
# UPDATE AVAILABILITY
# ============================================================

@app.post(
    "/items/<int:item_id>/availability"
)
def set_availability(item_id: int):

    # --------------------------------------------------------
    # B3 - Authorization
    # --------------------------------------------------------

    auth_error = check_authorization()

    if auth_error:

        return auth_error

    # --------------------------------------------------------
    # B1 - Accept
    # --------------------------------------------------------

    accept_error = check_accept()

    if accept_error:

        return accept_error

    # --------------------------------------------------------
    # Find item
    # --------------------------------------------------------

    item = store.find(item_id)

    if not item:

        return problem(
            404,
            "item-not-found",
            detail=f"Item {item_id} not found"
        )

    # --------------------------------------------------------
    # C3 - Idempotency-Key
    # --------------------------------------------------------

    key = request.headers.get(
        "Idempotency-Key"
    )

    # Use a separate namespace for availability keys.
    availability_key = None

    if key:

        availability_key = (
            f"availability:{key}"
        )

        prior = store.find_by_key(key)

        if prior:

            # If store already has this key,
            # return the existing result.
            response = jsonify({
                "itemId": prior.id,
                "isAvailable": prior.is_available
            })

            response.status_code = 202

            return response

    # --------------------------------------------------------
    # C2 - If-Match
    # --------------------------------------------------------

    current_etag = generate_etag(item)

    client_etag = request.headers.get(
        "If-Match"
    )

    if client_etag:

        if client_etag != current_etag:

            return problem(
                412,
                "precondition-failed",
                detail=(
                    "If-Match ETag does not match "
                    "current resource"
                )
            )

    # --------------------------------------------------------
    # Read request body
    # --------------------------------------------------------

    body = request.get_json(
        silent=True
    )

    if body is None:

        return problem(
            400,
            "invalid-request",
            detail="Malformed JSON request"
        )

    new_state = body.get(
        "isAvailable"
    )

    if not isinstance(
        new_state,
        bool
    ):

        return problem(
            400,
            "invalid-request",
            detail="isAvailable must be boolean"
        )

    # --------------------------------------------------------
    # B2 - State conflict
    # --------------------------------------------------------

    if item.is_available == new_state:

        return problem(
            409,
            "state-conflict",
            detail=f"Already set to {new_state}"
        )

    # --------------------------------------------------------
    # External sync
    # --------------------------------------------------------

    notify_external_sync_with_retry(
        item.id
    )

    # --------------------------------------------------------
    # Update state
    # --------------------------------------------------------

    item.is_available = new_state

    return jsonify({
        "itemId": item.id,
        "isAvailable": item.is_available
    }), 202


# ============================================================
# B6 - OPTIONS /items/{id}
# CORS PREFLIGHT
# ============================================================

@app.route(
    "/items/<int:item_id>",
    methods=["OPTIONS"],
    provide_automatic_options=False
)
def options_item(item_id: int):

    return "", 204, {

        # B2/A5
        "Allow": "GET, OPTIONS",

        # B6
        "Access-Control-Allow-Origin": "*",

        "Access-Control-Allow-Methods": (
            "GET, OPTIONS"
        ),

        "Access-Control-Allow-Headers": (
            "Content-Type, Authorization, Accept, "
            "Idempotency-Key, If-None-Match, If-Match"
        )
    }


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )