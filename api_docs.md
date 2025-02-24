####
# API Documentation

This API provides endpoints for the following resources:

## Users
- **GET /users**: Retrieve list of users.
- **GET /users/{user_id}**: Retrieve a single user.
- **POST /users**: Create a new user.
- **PUT /users/{user_id}**: Update an existing user.
- **DELETE /users/{user_id}**: Remove a user.

## Beers
- **GET /beers**: List all beers.
- **GET /beers/{beer_id}**: Get details of a specific beer.
- **POST /beers**: Add a new beer.

## Orders
- **GET /orders**: List all orders.
- **GET /orders/{order_id}**: Get order details.
- **POST /orders**: Create a new order.
- **PUT /orders/{order_id}**: Update an order.
- **DELETE /orders/{order_id}**: Cancel an order.

## Order Items
- **GET /orders/{order_id}/items**: List items in an order.
- **POST /orders/{order_id}/items**: Add an item to the order.

## Payments
- **GET /payments**: List all payment transactions.
- **GET /payments/{transaction_id}**: Get payment details.
- **POST /payments**: Create a new payment.

## Beer Sold
- **GET /beers_sold**: List beer sold transactions.
- **GET /beers_sold/{transaction_id}**: Get details of a specific beer sold record.

## Vip Customers
- **GET /vip_customers**: List VIP customers.
- **GET /vip_customers/{user_id}**: Get details for a VIP customer.
- **POST /vip_customers**: Add a new VIP customer.
