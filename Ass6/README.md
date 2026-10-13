# CS543 Assignment 6 — Orders Service

This folder contains a standalone implementation for the A6 handout. It is separate from `Ass5/` so the earlier assignment files remain unchanged.

## Important compatibility note

The supplied repository's `Ass5/service` implements a Catalogue Service with `/items` endpoints, while the A6 handout specifies an Orders Service with `/orders` endpoints. Because those are different APIs, this A6 implementation is isolated here rather than replacing your A5 code. Confirm with your instructor that a standalone Orders service is acceptable if A5 was expected to contain the Orders service.

## Run locally

Requires Python 3.10+ and internet access only if Flask is not already installed.

```bash
cd Ass6/service
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

In another terminal:

```bash
cd Ass6
python -m pytest -q
```

Service base URL: `http://127.0.0.1:5000`.

## Included behavior

- `POST /orders` returns `201` and `Location` on success.
- `GET /orders` and `GET /orders/{id}`.
- `PATCH /orders/{id}` applies a simple order-status transition map.
- `DELETE /orders/{id}` returns `204` when deletion is allowed.
- Consistent Problem Details errors using `application/problem+json; charset=utf-8`.
- Validation reports multiple bad fields in one `422` response.
- JSON by default, XML when requested, and `406` for unsupported `Accept` formats.
- `429` and the assignment-only `503` demonstration route include `Retry-After`.
- In-memory idempotency-key demonstration and automated tests.

## Before submitting

1. Add every team member's name and roll number to the first page/cover sheet as required by the assignment.
2. Start the service and run the tests on your computer.
3. Run the curl commands in `curl_commands.sh` and replace/update `transcript.txt` with the actual terminal output from your run.
4. Review `NOTES.md` against the behavior you observed.
5. The `payment_declined` and `available: false` fields are demonstration switches, not a real payment or menu integration. The store is in memory and resets when the process restarts; do not represent this as a production service.
