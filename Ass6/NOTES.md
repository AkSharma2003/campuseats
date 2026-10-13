# CS543 Assignment 6 — Notes

Team members :
- Name:- Piyush Lalchand Menghani  roll number: 20252651039
- Name:- Ankit Kumar Sharma        roll number: 20252651007
- Name:- Vivek Kumar Kosta         roll number: 20252651065
- Name:- Vijay Singh               roll number: 20252651064
- Name:- Shubham Gupta             roll number: 20252651021

## 1. Status map

- `POST /orders`: `201 Created` when an order is created; `400` for malformed JSON; `406` when the requested representation is unsupported; `415` when the body is not JSON; `422` for an empty cart or invalid fields; `402` for a declined payment; `409` for unavailable items; `429` when rate limited; `503` for transient service unavailability.
- `GET /orders`: `200 OK` with the order collection; `406` for an unsupported `Accept` type; `429` when rate limited.
- `GET /orders/{id}`: `200 OK` when found; `404` when the order does not exist; `406` for an unsupported `Accept` type.
- `PATCH /orders/{id}`: `200 OK` when a permitted transition succeeds; `404` when the order does not exist; `409` for an illegal transition; `422` when status is missing or invalid; `406` for an unsupported representation.
- `DELETE /orders/{id}`: `204 No Content` when deletion succeeds; `404` when missing; `409` when the order is in a state that cannot be deleted.
- `POST /admin/simulate-unavailable`: `503 Service Unavailable` demonstration endpoint; includes `Retry-After`. This is a testing hook, not a production endpoint.

## 2. Stable error type catalogue

- `empty-cart`: `POST /orders` has an empty or missing items array.
- `item-unavailable`: one or more requested items are marked unavailable.
- `payment-declined`: request sets the demo `payment_declined` flag; in a real integration this is driven by the payment provider.
- `order-not-found`: the requested order ID does not exist.
- `illegal-transition`: the requested status change is not allowed by the transition map.
- Additional types used by this implementation: `validation-error`, `not-acceptable`, `unsupported-media-type`, `rate-limit-exceeded`, `internal-error`, `not-found`, `method-not-allowed`.

## 3. Example Problem Details body

Example response for an unknown order (ID is illustrative):

```json
{
  "type": "order-not-found",
  "title": "Order Not Found",
  "status": 404,
  "detail": "No order exists with id missing-id."
}
```

`type` is the stable machine-readable identifier; `title` is the short summary; `status` mirrors the HTTP status; `detail` is a safe explanation. Error responses use `Content-Type: application/problem+json; charset=utf-8`.

## 4. Field-level 422 with two bad fields

Example request: `{"items":[{"id":"meal-1","qty":0}],"address":""}`.
The response contains `422` and an `errors` list naming both `items[0].qty` and `address`. See `transcript.txt` for captured output.

## 5. Retry safety

`GET /orders` and `GET /orders/{id}` are safe to retry because they do not change state. `POST /orders` should be retried only with the same `Idempotency-Key`; this implementation stores the key-to-order mapping in memory for the lifetime of the process. `PATCH` and `DELETE` are not generally safe to repeat without checking the current state. `429` and `503` include `Retry-After` and indicate a transient wait; do not blindly retry unchanged `4xx` validation or business errors. A production service should persist idempotency records and use an upstream payment idempotency key.

## 6. Internal errors and information hidden

Unexpected exceptions are logged server-side through Flask's exception logger and return a generic `500` Problem Details response. The caller does not receive a traceback, database message, file path, or other internal exception details. This standalone implementation uses in-memory storage, so no real database error can be triggered by the current data layer.

## 7. JSON and XML negotiation

Send `Accept: application/json` (or omit `Accept`) to receive JSON. Send `Accept: application/xml` to receive XML. Unsupported types return `406 Not Acceptable`. The XML output is a simple demonstration representation for this assignment; it is not a full XML schema contract.

## Implementation note

This `Ass6/service` is a standalone teaching Orders service added separately because the supplied A5 directory contains a Catalogue Service (`/items`), not the `/orders` service named by the assignment handout. Earlier assignments are preserved unchanged. Review the instructor's expected A5 Orders baseline before treating this as a drop-in replacement for that baseline.
