import os
import time
import random
import uuid
import requests
from flask import Flask, request, jsonify
import store
from errors import problem

app = Flask(__name__)


PAYMENTS_URL = os.environ.get("PAYMENTS_URL", "http://localhost:8080")


def notify_external_sync_with_retry(item_id: int):
    """Part D requirement: Hardened HTTP call with timeout, backoff & jitter"""
    key = str(uuid.uuid4())

    for attempt in range(3):
        try:
            r = requests.post(
                f"{PAYMENTS_URL}/payments",
                json={
                    "orderId": item_id,
                    "cardToken": "tok_sync",
                    "amount": 100,
                    "currency": "INR"
                },
                headers={"Idempotency-Key": key},
                timeout=2.0
            )

            if r.status_code in (200, 201):
                return r.json()

            if 400 <= r.status_code < 500:
                raise Exception("Client error (4xx) - DO NOT RETRY")

        except Exception as e:
            if attempt == 2 or "DO NOT RETRY" in str(e):
                break

            wait_time = (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(wait_time)


def validate(body: dict) -> list:
    errors = []

    if not isinstance(body.get("restaurantId"), int):
        errors.append(["restaurantId", "must be integer"])

    if not body.get("name") or not isinstance(body.get("name"), str):
        errors.append(["name", "required string"])

    price = body.get("pricePaise")

    if not isinstance(price, int) or price <= 0:
        errors.append(["pricePaise", "positive integer required"])

    return errors


@app.post("/items")
def create_item():
    body = request.get_json(silent=True) or {}

    errs = validate(body)

    if errs:
        return problem(400, "invalid-request", errors=errs)

    if body.get("name") == "BAD_ITEM":
        return problem(
            422,
            "domain-refusal",
            detail="Item domain policy failure"
        )

    key = request.headers.get("Idempotency-Key")

    if key:
        prior = store.find_by_key(key)

        if prior:
            return jsonify(prior.as_json()), 200

    item = store.create(
        body["restaurantId"],
        body["name"],
        body["pricePaise"],
        key
    )

    return jsonify(item.as_json()), 201, {
        "Location": f"/items/{item.id}"
    }


@app.get("/items/<int:item_id>")
def get_item(item_id: int):
    item = store.find(item_id)

    if not item:
        return problem(
            404,
            "item-not-found",
            detail=f"Item {item_id} not found"
        )

    return jsonify(item.as_json()), 200


@app.get("/items")
def list_items():
    rest_id = request.args.get("restaurantId", type=int)

    if rest_id is None:
        return problem(
            400,
            "invalid-request",
            detail="Missing restaurantId"
        )

    return jsonify(
        [i.as_json() for i in store.find_by_restaurant(rest_id)]
    ), 200


@app.post("/items/<int:item_id>/availability")
def set_availability(item_id: int):
    item = store.find(item_id)

    if not item:
        return problem(404, "item-not-found")

    body = request.get_json(silent=True) or {}

    new_state = body.get("isAvailable")

    if not isinstance(new_state, bool):
        return problem(400, "invalid-request")

    if item.is_available == new_state:
        return problem(
            409,
            "state-conflict",
            detail=f"Already set to {new_state}"
        )

    notify_external_sync_with_retry(item.id)

    item.is_available = new_state

    return jsonify({
        "itemId": item.id,
        "isAvailable": item.is_available
    }), 202


# A5: OPTIONS endpoint
@app.options("/items/<int:item_id>")
def options_item(item_id: int):
    return "", 204, {
        "Allow": "GET, OPTIONS"
    }