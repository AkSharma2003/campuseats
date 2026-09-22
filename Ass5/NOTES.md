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
