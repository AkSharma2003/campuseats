# CampusEats Assignment 5

## A1. CampusEats HTTP Method Map

| Action | HTTP Method | URL |
|---|---|---|
| Create a menu item | POST | /items |
| List menu items | GET | /items |
| Retrieve a single menu item | GET | /items/{id} |
| Update item availability | POST | /items/{id}/availability |

### Method Audit

- `POST /items` is used to create a new menu item.
- `GET /items` is used to read/list menu items.
- `GET /items/{id}` is used to retrieve a single menu item.
- `POST /items/{id}/availability` is used for the availability state transition.
- No action verb such as `/createItem`, `/getItem`, or `/updateAvailability` is present in the URL.

## A2. Non-CRUD Actions

The `POST /items/{id}/availability` endpoint models a non-CRUD action.

Changing an item's availability is a state transition rather than a simple create, read, update, or delete operation. Therefore, it is represented as a POST action on the item sub-resource:

`POST /items/{id}/availability`

This avoids using an action verb as the top-level URL, such as:

`POST /updateAvailability`

The request body contains the new availability state.

## A3. Safe and Idempotent Endpoints

| Endpoint | Safe | Idempotent | Explanation |
|---|---|---|---|
| GET /items | Yes | Yes | Reads the list of menu items without changing server state. |
| POST /items | No | No | Creates a new menu item; repeating the request may create another item. |
| GET /items/{id} | Yes | Yes | Reads one menu item without changing server state. |
| POST /items/{id}/availability | No | No | Changes the availability state of the item. |

### Retry Safety

The GET endpoints are naturally safe to retry because they only read data and do not modify server state.

`POST /items` is not naturally retry-safe because repeating a create request can create duplicate menu items.

`POST /items/{id}/availability` changes server state and is therefore not treated as naturally retry-safe. The retry-safety mechanism for this operation will be addressed in Part C.


## A4. Query Parameters for Reads

The menu item list endpoint remains a GET because it is a pure read operation.

Filtering, sorting, and pagination are handled through query parameters.

Example:

`GET /items?restaurantId=10&sort=pricePaise&order=asc&page=1&limit=20`

| Query Parameter | Purpose |
|---|---|
| restaurantId | Filter items by restaurant |
| sort | Select the field used for sorting |
| order | Select ascending or descending order |
| page | Select the result page |
| limit | Number of items returned per page |

## A5. OPTIONS and Method Override

The `/items/{id}` resource supports an OPTIONS operation.

A successful OPTIONS request returns status `204` with an `Allow` header describing the supported methods:

`Allow: GET, OPTIONS`

If a constrained client cannot send the required HTTP method, the documented fallback is the `X-HTTP-Method-Override` header. The client must use this only when the server explicitly supports this behavior.

## A6. Complete HTTP Request/Response Exchange

### Request

```http
POST /items HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Accept: application/json
Idempotency-Key: a6-demo-001

{
  "restaurantId": 1,
  "name": "Veg Burger",
  "pricePaise": 12000
}

```

### Response

HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.8 Python/3.14.5
Date: Tue, 22 Sep 2026 14:08:31 GMT
Content-Type: application/json
Content-Length: 156
Location: /items/1
Connection: close

{
  "createdAt": "2026-09-22T14:08:31.071476+00:00",
  "id": 1,
  "isAvailable": true,
  "name": "Veg Burger",
  "pricePaise": 12000,
  "restaurantId": 1
}


## B1. JSON Content Negotiation

CampusEats API responses use `application/json` for JSON response bodies.

The API supports `Accept: application/json`. If the client requests an unsupported response format, the API returns `406 Not Acceptable` with a JSON error response.

Example:

`Accept: application/json` → `200 OK`

`Accept: text/html` → `406 Not Acceptable`

The `406` response also uses:

`Content-Type: application/json`

Large JSON response compression using gzip is not currently enabled in the Flask service.



## B2. HTTP Status Codes

The CampusEats service uses the following HTTP status codes:

| Situation | Status Code |
|---|---|
| Successful resource creation | 201 Created |
| Successful resource retrieval | 200 OK |
| Successful deletion | 204 No Content |
| Malformed request | 400 Bad Request |
| Resource not found | 404 Not Found |
| State conflict | 409 Conflict |
| Domain validation/refusal | 422 Unprocessable Entity |

For successful creation, the response includes a `Location` header pointing to the newly created resource.

Example:

`Location: /items/2`


## B3. Authorization Header

Protected endpoints require the following authorization header:

`Authorization: Bearer <token>`

The service does not implement a real authentication or token-validation system for this assignment. It only checks that the Authorization header uses the Bearer format and contains a non-empty token.

The following cases return `401 Unauthorized`:

- Missing Authorization header
- Empty Bearer token
- Invalid Authorization format

## B4. ETag and Cache-Control

Single-item GET responses include an ETag and Cache-Control header.

Example:

`GET /items/1`

Response headers:

```text
ETag: "7f8c6d83ec2cb129aa388cb0f9d21585aadd752a4fccb66ec4636d3f59dc1e5f"
Cache-Control: private, max-age=60
```

## B5. Rate Limiting

The CampusEats service applies a per-client rate limit of 5 requests
within a 60-second window.

The client is identified using its IP address.

Successful responses include:

```text
X-RateLimit-Limit: 5
X-RateLimit-Remaining: <remaining requests>

When the client exceeds the limit, the service returns:
HTTP/1.1 429 TOO MANY REQUESTS
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
Retry-After: <seconds>

Example from testing:
Request 5:
HTTP/1.1 201 CREATED
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0

Request 6:
HTTP/1.1 429 TOO MANY REQUESTS
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
Retry-After: 59


## B6. CORS and OPTIONS Preflight

The CampusEats API supports Cross-Origin Resource Sharing (CORS).

The API includes the following CORS headers:

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept, Idempotency-Key, If-None-Match, If-Match

The /items/{id} resource supports an OPTIONS preflight request.

Example:
OPTIONS /items/1
Origin: http://localhost:3000
Access-Control-Request-Method: GET
Access-Control-Request-Headers: Authorization,Content-Type

The server responds with:
HTTP/1.1 204 NO CONTENT
Allow: GET, OPTIONS
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept, Idempotency-Key, If-None-Match, If-Match

## B7. Security Headers

The CampusEats API includes the following security-related response headers:

```text
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains

X-Content-Type-Options: nosniff prevents browsers from MIME-sniffing the response content type.

Strict-Transport-Security instructs compatible browsers to use HTTPS for future requests.

The development server also provides the standard Server and Date response headers. The following headers were observed during testing:
Server: Werkzeug/3.1.8 Python/3.14.5
Date: Tue, 22 Sep 2026 15:01:06 GMT

B7 Test Result

Request:
GET /items/1 HTTP/1.1
Accept: application/json

Response:

HTTP/1.1 404 NOT FOUND
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains

## C1. Conditional GET with If-None-Match

The single-item GET endpoint supports conditional requests using the `If-None-Match` header.

The server first returns an ETag with the resource:

```text
ETag: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"

When the client sends the same ETag using If-None-Match, the server returns 304 Not Modified without sending the JSON response body.

Request:
GET /items/1 HTTP/1.1
Accept: application/json
If-None-Match: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"

Response:
HTTP/1.1 304 NOT MODIFIED
ETag: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"
Cache-Control: private, max-age=60


## C2. Conditional Write with If-Match

The availability update endpoint supports conditional writes using the `If-Match` header.

The client must provide the current ETag of the resource when updating it. If the supplied ETag does not match the current resource ETag, the server rejects the update with `412 Precondition Failed`.

Test request:

```text
POST /items/1/availability HTTP/1.1
If-Match: "wrong-etag-12345"
Content-Type: application/json
Accept: application/json
Authorization: Bearer demo-token

Request body:
{
  "isAvailable": false
}

Response:

HTTP/1.1 412 PRECONDITION FAILED
Content-Type: application/json

Response body:
{
  "detail": "If-Match ETag does not match current resource",
  "status": 412,
  "title": "Error",
  "type": "/errors/precondition-failed"
}


## C3. Idempotency-Key

The `POST /items` create endpoint supports the `Idempotency-Key` header.

A client can provide a unique idempotency key when creating a menu item. If the same request is retried with the same key, the service returns the original result instead of creating another item.

### First Request

```text
POST /items HTTP/1.1
Authorization: Bearer demo-token
Content-Type: application/json
Accept: application/json
Idempotency-Key: c3-demo-001

Response:
HTTP/1.1 201 CREATED
Location: /items/2

Response body:
{
  "createdAt": "2026-09-22T16:25:32.801530+00:00",
  "id": 2,
  "isAvailable": true,
  "name": "C3 Idempotency Test",
  "pricePaise": 7000,
  "restaurantId": 1
}

Repeated Request

The exact same request was sent again using:

Idempotency-Key: c3-demo-001
The service returned:
HTTP/1.1 201 CREATED
Location: /items/2

with the same resource representation and id: 2.

Therefore, the retry did not create a duplicate menu item and returned the original result.

Where Duplicate Work Would Cause Real Damage


## C4. Safe-Retry Plan

The following retry plan is based on whether an endpoint is safe/idempotent and whether repeating the operation can cause duplicate work.

| Endpoint | Operation Risk | Retry Mechanism | Why |
|---|---|---|---|
| GET /items | Low | No special mechanism required | GET is safe and can be retried without changing server state. |
| GET /items/{id} | Low | If-None-Match | The client can use the ETag to avoid downloading an unchanged resource. |
| POST /items | High | Idempotency-Key | A retry of a create request could otherwise create a duplicate menu item. |
| POST /items/{id}/availability | Medium | If-Match | The client can ensure that the resource has not changed since the ETag was obtained before applying the update. |

### Retry Strategy

- Safe GET requests can normally be retried because they do not modify server state.
- `POST /items` should use an `Idempotency-Key` when a client may retry the request.
- `GET /items/{id}` can use `If-None-Match` with the previously received ETag.
- `POST /items/{id}/availability` should use `If-Match` with the current ETag to prevent updates based on a stale representation.

These mechanisms reduce the risk of duplicate work or overwriting a resource based on outdated information.

## D2. HTTP Headers Table

The following table documents the important request and response headers used by each CampusEats endpoint.

| Endpoint | Request Headers | Response Headers |
|---|---|---|
| POST /items | Authorization, Content-Type, Accept, Idempotency-Key | Content-Type, Location, X-RateLimit-Limit, X-RateLimit-Remaining, Access-Control-Allow-Origin, X-Content-Type-Options, Strict-Transport-Security |
| GET /items | Accept | Content-Type, Access-Control-Allow-Origin, X-Content-Type-Options, Strict-Transport-Security |
| GET /items/{id} | Accept, If-None-Match | Content-Type, ETag, Cache-Control, Access-Control-Allow-Origin, X-Content-Type-Options, Strict-Transport-Security |
| POST /items/{id}/availability | Authorization, Content-Type, Accept, If-Match, Idempotency-Key | Content-Type, Access-Control-Allow-Origin, X-Content-Type-Options, Strict-Transport-Security |
| OPTIONS /items/{id} | Origin, Access-Control-Request-Method, Access-Control-Request-Headers | Allow, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers, X-Content-Type-Options, Strict-Transport-Security |

### Important Header Purposes

- `Authorization: Bearer <token>` protects endpoints that require authorization.
- `Content-Type: application/json` identifies JSON request bodies.
- `Accept: application/json` requests JSON responses.
- `Idempotency-Key` prevents duplicate work when a create request is retried.
- `If-None-Match` is used for conditional GET requests.
- `If-Match` prevents updates based on a stale ETag.
- `ETag` identifies the current representation of a resource.
- `Cache-Control` controls client-side caching of single-item responses.
- `Location` identifies the newly created resource after a successful `POST`.
- `X-RateLimit-Limit` and `X-RateLimit-Remaining` communicate the rate-limit budget.
- `Retry-After` is returned when the rate limit is exceeded.
- `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers` support CORS.
- `X-Content-Type-Options: nosniff` prevents MIME-type sniffing.
- `Strict-Transport-Security` instructs compatible browsers to prefer HTTPS.




## D3. Final Documentation

### 1. Three Endpoint Method, Success Status, and Important Header

| Endpoint                        | Method | Success Status | Most Important Response Header | Why                                                                                                        |
| ------------------------------- | ------ | -------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `POST /items`                   | POST   | `201 Created`  | `Location`                     | It tells the client where the newly created resource can be retrieved.                                     |
| `GET /items/{id}`               | GET    | `200 OK`       | `ETag`                         | It identifies the current representation and enables conditional requests such as `If-None-Match`.         |
| `POST /items/{id}/availability` | POST   | `202 Accepted` | `ETag`                         | The ETag represents the current resource version and can be used with `If-Match` to prevent stale updates. |

---

### 2. Safe and Idempotent Endpoints

| Endpoint                        | Safe | Idempotent                  | Explanation                                           |
| ------------------------------- | ---- | --------------------------- | ----------------------------------------------------- |
| `GET /items`                    | Yes  | Yes                         | Only reads the list and does not change server state. |
| `GET /items/{id}`               | Yes  | Yes                         | Only reads a single resource.                         |
| `POST /items`                   | No   | No                          | Each normal request can create a new resource.        |
| `POST /items/{id}/availability` | No   | Not naturally safe to retry | It changes the item's availability state.             |

The GET endpoints are both safe and idempotent because repeating the same request does not modify server state.

`POST /items` is neither safe nor naturally idempotent because repeating the request can create duplicate menu items.

To make the create operation retry-safe, the service supports the `Idempotency-Key` request header. When the same key is sent again, the service returns the original created resource instead of creating another resource.

For conditional availability updates, `If-Match` is used so that an update based on a stale resource version is rejected with `412 Precondition Failed`.

---

### 3. ETag, 304, and 412

Example ETag returned by the service:

```text
ETag: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"
```

#### Conditional GET

Request:

```http
GET /items/1 HTTP/1.1
Host: localhost:8080
Accept: application/json
If-None-Match: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"
```

Response:

```http
HTTP/1.1 304 NOT MODIFIED
ETag: "c95d628d00fb1dfa5228ab22c4a7dc14059cab3e5d47bd232a4fa54e0fdc2ec7"
Cache-Control: private, max-age=60
```

The `304 Not Modified` response saves bandwidth because the server does not resend the unchanged JSON representation.

#### Conditional Write

Request:

```http
POST /items/1/availability HTTP/1.1
Host: localhost:8080
Authorization: Bearer demo-token
Content-Type: application/json
Accept: application/json
If-Match: "wrong-etag-12345"

{
  "isAvailable": false
}
```

Response:

```http
HTTP/1.1 412 PRECONDITION FAILED
Content-Type: application/json
```

The `412` prevents an update from being performed using a stale or incorrect resource version. This helps prevent lost updates when another client has changed the resource.

---

### 4. Difference Between 422 and 400

#### 400 Bad Request

Example request:

```http
POST /items HTTP/1.1
Host: localhost:8080
Authorization: Bearer demo-token
Content-Type: application/json
Accept: application/json

{
  "restaurantId": 1,
  "name": "Bad Request Test",
  "pricePaise": "wrong"
}
```

The request is syntactically readable JSON, but `pricePaise` has an invalid type. The service returns:

```http
HTTP/1.1 400 BAD REQUEST
```

`400 Bad Request` is used for malformed or invalid request data.

#### 422 Unprocessable Entity

Example request:

```http
POST /items HTTP/1.1
Host: localhost:8080
Authorization: Bearer demo-token
Content-Type: application/json
Accept: application/json

{
  "restaurantId": 1,
  "name": "BAD_ITEM",
  "pricePaise": 5000
}
```

The request structure is valid, but the application rejects the value because it violates a domain/business rule. The service returns:

```http
HTTP/1.1 422 UNPROCESSABLE ENTITY
```

Therefore, `400` is used for invalid request structure/data, while `422` is used when the request is understood but cannot be accepted because of a domain rule.

---

### 5. Browser CORS Error

If a browser page from another origin calls the CampusEats API and the server logs show `200 OK`, the browser can still block the response from being made available to the web page.

The browser's same-origin policy/CORS enforcement is responsible for blocking the page from reading the response.

The response header that allows the cross-origin request is:

```http
Access-Control-Allow-Origin: *
```

The service also handles CORS preflight requests with `OPTIONS` and returns:

```http
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept, Idempotency-Key, If-None-Match, If-Match
```

---

### 6. Cache-Control and No-Store

For a single menu item response, the service uses:

```http
Cache-Control: private, max-age=60
```

Example:

```http
GET /items/1
```

This allows a private client cache to reuse the representation for up to 60 seconds, while the ETag can be used to validate whether the resource changed.

For sensitive responses containing credentials, payment information, tokens, or other private data, the appropriate directive would be:

```http
Cache-Control: no-store
```

`no-store` prevents caches from storing the response and is appropriate when retaining the response could expose sensitive information.

---

### 7. When POST Would Be Appropriate for Search

The CampusEats search/list operation is currently a GET because filtering, sorting, and pagination can be represented using query parameters:

```http
GET /items?restaurantId=10&sort=pricePaise&order=asc&page=1&limit=20
```

POST could be appropriate when the search request becomes complex and cannot reasonably be represented as a query string, for example when it contains a large structured search document with many nested filters.

For example:

```http
POST /items/search
Content-Type: application/json
```

with a JSON search body.

However, switching from GET to POST gives up some advantages of GET, including straightforward URL sharing/bookmarking, conventional safe/read semantics, and easier HTTP caching.

Therefore, GET remains appropriate for the current CampusEats filtering, sorting, and pagination requirements.

---

### 8. Meaning of Location on 201 and 3xx

For a successful resource creation:

```http
HTTP/1.1 201 Created
Location: /items/3
```

the `Location` header identifies the newly created resource. The client can use `/items/3` to retrieve that resource.

For a `3xx` redirect response, the `Location` header identifies the target URI to which the client should redirect or continue the request, depending on the specific `3xx` status code.

Therefore:

* `201 + Location` → identifies the newly created resource.
* `3xx + Location` → identifies the redirect target.


### Team Information

**Team ID:** []

**Team Members:**

| Roll No.    | Name                      |
| ----------- | ------------------        |
| 20252651007 | Ankit Kumar Sharma        |
| 20252651039 | Piyush Lalchand Menghani  |
| 20252651064 | Vijay Singh               |
| 20252651065 | Vivek Kumar Kosta         |
| 20252651021 | Shubham Gupta             |

