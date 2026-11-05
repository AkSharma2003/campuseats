
# CampusEats REST API - Assignment 8

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

## Assignment Questions and Answers

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

## Team Members

Add all team members' names and roll numbers here.

## Demonstration Video

Add Google Drive demonstration video link here.

## Screenshots

Add the before and after screenshots of the menu here.
