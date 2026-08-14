# HTTP Log

## Request 1 — Get Post 1

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

### Response

```text
HTTP/2 200 
date: Fri, 14 Aug 2026 17:17:40 GMT
content-type: application/json; charset=utf-8
content-length: 292
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785194657"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785194657"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785194663
age: 20410
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b19d483d4d3a15-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}  
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.



## Request 2 — Get Post 2

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/posts/2
```

### Response

```text
HTTP/2 200 
date: Fri, 14 Aug 2026 17:35:09 GMT
content-type: application/json; charset=utf-8
content-length: 278
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"116-jnDuMpjju89+9j7e0BqkdFsVRjs"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=QLiSye1cwBbJeXgFNCBUxgevbRgIRWjlLgw4ygV1udE%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786354973"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=QLiSye1cwBbJeXgFNCBUxgevbRgIRWjlLgw4ygV1udE%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786354973"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786355034
age: 21774
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b1b6e2fd5ee565-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 2,
  "title": "qui est esse",
  "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.




## Request 3 — Get User 1

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/users/1
```

### Response

```text
HTTP/2 200 
date: Fri, 14 Aug 2026 17:42:41 GMT
content-type: application/json; charset=utf-8
content-length: 509
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=c4W1UxriyoWTYFuUhbAlZOrDzICU7r%2BRoXsXRciuS0Y%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786374767"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=c4W1UxriyoWTYFuUhbAlZOrDzICU7r%2BRoXsXRciuS0Y%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786374767"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786374775
age: 7224
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b1c1ed8bd6d8ea-BOM
alt-svc: h3=":443"; ma=86400

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.