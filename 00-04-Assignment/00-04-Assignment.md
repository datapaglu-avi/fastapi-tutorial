# 📘 Mini Project: Product Review API

You're building a simple backend for a product catalog system.

---

## 🛠️ Features

### ✅ 1. Add a Product
- **Endpoint:** `POST /products/`
- **Request Body:**
  ```json
  {
    "name": "Macbook Air",
    "description": "Apple laptop",
    "price": 1099.99,
    "in_stock": true
  }
  ```

---

### ✅ 2. Get a Product by ID
- **Endpoint:** `GET /products/{product_id}`
- `product_id`: **Path Parameter** (int)

---

### ✅ 3. List All Products with Optional Pagination
- **Endpoint:** `GET /products/`
- **Query Parameters:**
  - `skip: int = 0`
  - `limit: int = 10`

---

### ✅ 4. Update a Product by ID
- **Endpoint:** `PUT /products/{product_id}`
- **Path Parameter:**
  - `product_id: int`
- **Request Body:** (Same as POST `/products/`)
- **Query Parameter:**
  - `notify: bool = False`  
  - If `notify=true`, include `"notification": "Product updated!"` in the response.

---

### ✅ 5. Add a Review to a Product
- **Endpoint:** `POST /products/{product_id}/reviews/`
- **Request Body:**
  ```json
  {
    "reviewer": "Alice",
    "rating": 4.5,
    "comment": "Great build quality."
  }
  ```

---

### ✅ 6. Get All Reviews for a Product
- **Endpoint:** `GET /products/{product_id}/reviews/`
- **Optional Query Parameter:**
  - `min_rating: float | None = None`
  - If provided, only return reviews with `rating >= min_rating`

---

## 💾 In-Memory Storage
Use simple Python lists/dicts to store the products and their reviews. No database needed.

---

## 💡 Bonus (Optional)
- Validate that:
  - `price > 0`
  - `rating` is between `0.0–5.0` using Pydantic constraints
- Implement:
  - `DELETE /products/{product_id}` to remove a product
