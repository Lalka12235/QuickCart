# QuickCart

QuickCart is a minimalistic but functional API for an online store, including:
- ✅ Products (adding, viewing, filtering)
- ✅ Shopping cart (adding/removing products)
- ✅ Orders (checkout, history)

## 🛠 Tech Stack

- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker




# Docs
## 👤 Users (/users)

 - GET /users/{email} — get user by email

 - POST /users — create new user

 - DELETE /users — delete user by email and password

## 📦 Products (/products)

 - GET /products — get list of products with pagination (offset, limit)

 - GET /products/count — get total number of products

 - GET /products/{title} — get product by name

 - POST /products — create new product

 - PUT /products/{title} — update product data

 - PATCH /products/{title} — change product quantity (delta)

 - DELETE /products/{title} — delete product by name

## 🛒 Orders (/orders)

 - GET /orders{order_id} — get order by order_id and email ❗ (possibly route error: / is missing)

 - GET /orders/{user_id} — get all orders of the user

 - POST /orders — create an order (email + OrderSchema)

 - PATCH /orders/{order_id} — change the delivery status

 - DELETE /orders — cancel an order

 - GET /orders/count — the number of all orders of the user

## ⭐ Reviews (/reviews)

 - GET /reviews/{user_id}/{title} — get a user review of the product

 - GET /reviews — get all reviews of the user

 - POST /reviews — add a review (email + title + body)

 - PUT /reviews/{user_id}/{title} — update a review

 - DELETE /reviews/{user_id}/{title} — delete a review

 - GET /reviews/{title_product} — get all reviews of the product

 - GET /reviews/avg/{title_product} — calculate average product rating

 - GET /reviews/pagination/{title_product} — get product reviews with pagination 


# Deployment
Docker build
```bash
  docker-compose up -d --build

```
Path api
```bash
  http://localhost:80/docs
```

Stop 
```bash
  docker-compose down
```
