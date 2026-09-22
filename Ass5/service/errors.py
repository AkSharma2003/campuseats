from flask import jsonify

TITLES = {
    "invalid-request": "Invalid request",
    "item-not-found": "Item not found",
    "state-conflict": "State conflict",
    "domain-refusal": "Domain refusal"
}

def problem(status: int, code: str, detail: str = "", errors: list = None):
    body = {
        "type": f"/errors/{code}",
        "title": TITLES.get(code, "Error"),
        "status": status,
        "detail": detail
    }
    if errors:
        body["errors"] = errors
    return jsonify(body), status