# CampusEats Brief

## What

CampusEats is a food ordering and delivery system designed for a campus environment. Students can log in, manage their profile and delivery addresses, browse campus restaurants and their menus, add food items to a cart, and place orders. They can pay online and track their delivery after a rider is assigned. The system also sends notifications when an order is placed, paid, on the way, and delivered.

The system is organized into six main services: Accounts, Catalogue, Orders, Payments, Delivery, and Notifications. Each service has a clear responsibility and manages its own data.

## Who

- **Students** — browse food, manage their accounts, place orders, pay online, and track deliveries.
- **Campus Restaurants** — provide restaurants, menus, food items, and prices.
- **Riders** — are assigned to orders and deliver food to students.
- **CampusEats Services** — work together to complete the food ordering and delivery process.

## Nouns

The main **nouns** (things/data in the system) are:

- Student
- User profile
- Delivery address
- Restaurant
- Menu
- Food item
- Price
- Cart
- Order
- Order status
- Payment
- Transaction
- Refund
- Rider
- Delivery assignment
- Notification
- Message

## Verbs

The main **verbs** (actions/tasks/contracts) are:

- Log in
- Manage profile
- Manage delivery addresses
- Browse restaurants
- Browse menus
- Check item availability and price
- Add items to cart
- Place an order
- Get order details
- Cancel an order
- Pay / charge payment
- Refund payment
- Assign a rider
- Track delivery
- Send notifications

## Summary

CampusEats connects students with campus restaurants so they can order food, pay for it, and receive or track their delivery. The system separates these responsibilities into different services, with each service providing specific operations while hiding its internal implementation.