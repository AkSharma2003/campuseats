
# CampusEats REST API - Assignment 8
## Team Members
- Name:- Piyush Lalchand Menghani  roll number: 20252651039
- Name:- Ankit Kumar Sharma        roll number: 20252651007
- Name:- Vivek Kumar Kosta         roll number: 20252651065
- Name:- Vijay Singh               roll number: 20252651064
- Name:- Shubham Gupta             roll number: 20252651021
## Selected CampusEats Service

We selected the Menu / Catalogue Service.

This service allows users to view food items and add new dishes using a Node.js and Express REST API.

## Technologies Used

- Node.js
- Express.js
- HTML5
- CSS3
- JavaScript
- REST API
- JSON

## Features

- Display all menu items.
- Retrieve one dish using its ID.
- Add a new dish using a form.
- Validate required input fields.
- Display appropriate HTTP status codes.
- Serve the frontend using Express static middleware.

## Project Structure

```text
Ass8/
├── public/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── server.js
├── package.json
├── package-lock.json
└── README.md
```

## API Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | /items | Get all dishes |
| GET | /items/:id | Get one dish |
| POST | /items | Add a new dish |

## HTTP Status Codes

- 200 OK: Successful GET request.
- 201 Created: New dish successfully added.
- 404 Not Found: Dish ID does not exist.
- 422 Unprocessable Content: Required name is missing or invalid.

## Installation

Install dependencies:

```bash
npm install
```

Start the server:

```bash
npm start
```

Open the application:

http://localhost:3000

# CampusEats REST API - Assignment 9

## Team Members
- Name:- Piyush Lalchand Menghani  roll number: 20252651039
- Name:- Ankit Kumar Sharma        roll number: 20252651007
- Name:- Vivek Kumar Kosta         roll number: 20252651065
- Name:- Vijay Singh               roll number: 20252651064
- Name:- Shubham Gupta             roll number: 20252651021

### 1. Which CampusEats service did you pick, and what are its routes (method + path)?

We selected the Menu / Catalogue Service.

Its REST API routes are:

- GET /items - Retrieves the complete menu.
- GET /items/:id - Retrieves a specific dish using its ID.
- POST /items - Creates a new dish.

### 2. Which status codes did you return, and for which outcomes?

- 200 OK: Returned when dishes are successfully retrieved.
- 201 Created: Returned when a new dish is successfully added.
- 404 Not Found: Returned when a requested dish ID does not exist.
- 422 Unprocessable Content: Returned when the required dish name is missing or invalid.

### 3. Where did you use req.params and where req.body? Why does POST need express.json()?

We used req.params.id in GET /items/:id to retrieve the dish ID from the URL.

We used req.body in POST /items to access the new dish information sent by the client.

express.json() is required because it parses incoming JSON request bodies and makes the data available through req.body.

## Data Storage

The project uses an in-memory JavaScript array containing four initial menu records.

The data is temporary and resets when the server restarts.


# Assignment 9 - Securing the API

## Security Features

1. User authentication using JWT.
2. Password hashing using bcryptjs.
3. Login endpoint: POST /login.
4. JWT verification middleware.
5. Role-based authorization middleware.
6. Protected GET /items route.
7. Protected GET /items/:id route.
8. Protected POST /items route.

## Seeded Users

| Email | Password | Role |
|---|---|---|
| customer@campuseats.com | customer123 | customer |
| restaurant@campuseats.com | restaurant123 | restaurant |

## API Routes

| Method | Endpoint | Authentication | Authorization |
|---|---|---|---|
| POST | /login | No | No |
| GET | /items | Yes | Any authenticated user |
| GET | /items/:id | Yes | Any authenticated user |
| POST | /items | Yes | restaurant or admin |

## HTTP Status Codes

- 200: Successful login or GET request.
- 201: New menu item created.
- 401: Missing, invalid or expired token / invalid credentials.
- 403: Insufficient permissions.
- 404: Dish not found.
- 422: Invalid input.

## Password Security

Passwords are hashed using bcryptjs.
Plain-text passwords are not stored.

## JWT Security

JWT tokens are signed using a secret key
and expire after one hour.

## Testing

All security scenarios were tested using Postman.

Screenshots demonstrate:
- Missing token returns 401.
- Successful login returns JWT.
- Authenticated GET returns 200.
- Customer POST returns 403.
- Restaurant POST returns 201.



## GitHub Repository

https://github.com/AkSharma2003/campuseats.git

## login as a customer:

Email	customer@campuseats.com
Password	customer123

## login as a restaurant:

Email	restaurant@campuseats.com
Password	restaurant123

## JWT Token

$env:JWT_SECRET="campuseats_assignment09_secret_2026"