# CampusEats — Assignment 7: GraphQL with MySQL

## Team Members
- Name:- Piyush Lalchand Menghani  roll number: 20252651039
- Name:- Ankit Kumar Sharma        roll number: 20252651007
- Name:- Vivek Kumar Kosta         roll number: 20252651065
- Name:- Vijay Singh               roll number: 20252651064
- Name:- Shubham Gupta             roll number: 20252651021


## Selected CampusEats Service
We selected the **Dish/Menu Management Service**. It allows clients to retrieve dishes and add or update dish information using GraphQL, with MySQL as the database.

## Technologies Used
- Node.js and Express
- Apollo Server and GraphQL
- MySQL
- HTML, CSS and JavaScript

## How to Run
1. Install Node.js and MySQL.
2. Create the database and tables by running `schema.sql`.
3. Create a `.env` file using `.env.example` and configure your local MySQL credentials.
4. Install dependencies using `npm install`.
5. Start the application using `npm start`.
6. Open `http://localhost:4000` for the frontend or `http://localhost:4000/graphql` for the GraphQL interface.

**Important:** Do not commit `.env` or expose database passwords.

## Assignment Questions and Answers

### 1. Which CampusEats service did you pick?
We picked the Dish/Menu Management Service, which lets clients view dishes and add or update dish details.

### 2. Name one field a client can skip and one it cannot. Why do we use the `!` sign?
A client can skip the `available` field when selecting fields in a GraphQL query if it does not need that value. A client cannot omit a required input field such as `name` when adding a dish if the schema defines it as `String!`.

The `!` symbol means the type is non-null. It indicates that a required input cannot be null and that a non-null output must return a value.

### 3. Map the query to SQL. Which part became the WHERE clause, and which resolver ran INSERT?
The `id` argument in the `dish(id: ...)` query is used by the resolver to look up a specific dish with SQL similar to `WHERE id = ?`. The `addDish` mutation resolver runs the SQL `INSERT` statement to add a new dish to the MySQL database.

## Demonstration Video
Google Drive link: [Paste your demonstration video link here]

## Screenshots
- Before mutation: [Add/link screenshot showing the initial dish list]
- After mutation: [Add/link screenshot showing the newly added dish]
