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



## Request 2 — Get Comments 1

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/comments/1
```

### Response

```text
HTTP/2 200 
date: Sat, 15 Aug 2026 11:38:10 GMT
content-type: application/json; charset=utf-8
content-length: 268
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"10c-KJ4I9RM/+33TKdV8CFsIvqsDSP0"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=bB%2BN%2FFUdyCDto4SqNATX66bYsXSTyfHVG%2BrJgswnemI%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786780972"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=bB%2BN%2FFUdyCDto4SqNATX66bYsXSTyfHVG%2BrJgswnemI%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786780972"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786781023
age: 12918
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b7e95aaf60cc07-BOM
alt-svc: h3=":443"; ma=86400

{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.




## Request 3 — Get Albums 1

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/albums/1
```

### Response

```text
HTTP/2 200 
date: Sat, 15 Aug 2026 11:41:04 GMT
content-type: application/json; charset=utf-8
content-length: 64
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"40-74G1+b66MteeTYAz6G+NybtDGFA"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=f8weDUDZjLeMjOQp%2FE6wmwCnoeHSeVctLVxa6z9m45o%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785412055"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=f8weDUDZjLeMjOQp%2FE6wmwCnoeHSeVctLVxa6z9m45o%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785412055"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785412056
age: 2926
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b7ed99aeefb87c-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "quidem molestiae enim"
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.



## Request 4 — Get Comments 1

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/comments/1
```

### Response

```text
HTTP/2 200 
date: Fri, 14 Aug 2026 17:49:22 GMT
content-type: application/json; charset=utf-8
content-length: 268
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"10c-KJ4I9RM/+33TKdV8CFsIvqsDSP0"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=xdWkQvXg9gANlArctYa9YcGE%2FFvv3ms8I9qeRCvs0w0%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786714968"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=xdWkQvXg9gANlArctYa9YcGE%2FFvv3ms8I9qeRCvs0w0%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786714968"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786714990
age: 14793
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b1cbb68ea2f7e1-BOM
alt-svc: h3=":443"; ma=86400

{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.



## Request 5 — Get Posts 999999

### Request

```bash
curl -i https://jsonplaceholder.typicode.com/posts/999999
```

### Response

```text
HTTP/2 404 
date: Fri, 14 Aug 2026 17:52:36 GMT
content-type: application/json; charset=utf-8
content-length: 2
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=aMyNV1ofdVtIwRe1K%2Bk5FVH3Ho4uDaju1dKhPH9cnFM%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786729956"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=aMyNV1ofdVtIwRe1K%2Bk5FVH3Ho4uDaju1dKhPH9cnFM%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786729956"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786729990
cf-cache-status: EXPIRED
cf-ray: a2b1d0706bedc795-BOM
alt-svc: h3=":443"; ma=86400

{}
```
**Status:** `404 Not Found` means the requested resource does not exist on the server.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.