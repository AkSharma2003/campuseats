# CS543 Assignment 4 Notes

**Team Details:**
* **Name:** [Your Name] | **Roll No:** [Your Roll No]
* **Partner Name:** [Partner Name] | **Roll No:** [Partner Roll No]

---

## Resource Table (A4)
| Method | URL | What it does | Success Code | Failure Codes |
| :--- | :--- | :--- | :--- | :--- |
| POST | /items | Creates a new menu item | 201 | 400, 422 |
| GET | /items/{id} | Reads a single item | 200 | 404 |
| GET | /items | Lists items filtered by restaurantId | 200 | 400 |
| POST | /items/{id}/availability | Updates item availability state | 202 | 404, 409 |

---

## A5 Justification
The operation `setAvailability` was mapped to a sub-resource `/items/{id}/availability` using POST because state transitions require specific domain logic. Actions as query strings or over-generic PATCH updates were rejected to avoid obscuring state changes.

---

## D3 Fallback Reasoning
When the external dependency is unreachable, the Catalogue service fails fast with HTTP 503 instead of degrading silently. Degrading locally would lead to inconsistent data states across dependent services.

---

## Answers to Assignment Questions

### 1. Line Count & WSDL vs OpenAPI Comparison
* **WSDL Line Count:** ~150 lines (Assignment 3)
* **OpenAPI Line Count:** ~60 lines (`openapi.yaml`)
* **Difference Breakdown:** WSDL requires heavy XML namespace declarations, explicit message wrappers (`<wsdl:message>`), and protocol bindings (`<wsdl:binding>`). OpenAPI uses concise YAML syntax and maps directly to native HTTP methods.
* **Two Omitted Things in OpenAPI:**
  1. `<wsdl:binding>` (mapping operations to SOAP HTTP transport protocols)
  2. `<wsdl:message>` (separate input/output message element definitions)

### 2. SOAP Fault vs HTTP Status Codes
* **Assignment 3 SOAP Fault Example:**
  ```xml
  <soapenv:Fault>
      <faultcode>soapenv:Client</faultcode>
      <faultstring>Invalid Item Price</faultstring>
  </soapenv:Fault>