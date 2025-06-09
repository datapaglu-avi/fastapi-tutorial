from typing import Union
from fastapi import FastAPI  # type: ignore
from pydantic import BaseModel  # type: ignore

# Initialize FastAPI app
app = FastAPI()


# Define the schema for the request body using Pydantic
class Item(BaseModel):
    name: str               # Required field: name of the item
    price: float            # Required field: price of the item
    is_offer: Union[bool, None] = None  # Optional field: whether the item is on offer


@app.get("/")
def read_root():
    # Root endpoint: returns a basic greeting
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    GET /items/{item_id}

    - `item_id` is a **required path parameter**
    - `q` is an **optional query parameter**
    - Example usage: http://127.0.0.1:8000/items/7?q=avi → {"item_id":7,"q":"avi"}
    - Interactive API docs available at: http://127.0.0.1:8000/docs
    """
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    PUT /items/{item_id}

    - `item_id` is a **required path parameter**
    - `item` is a **required request body** of type `Item`
    - Example JSON body:
        {
            "name": "Some Item",
            "price": 99.99,
            "is_offer": true
        }
    
    - Note: If you want the body to be optional, use:
        item: Union[Item, None] = None
    """
    return {"item_name": item.name, "item_id": item_id}


# ───────────────────────────────
# 📌 SUMMARY / KEY TAKEAWAYS
# ───────────────────────────────

# ✅ Path Parameters:
# - `item_id` is required for both GET and PUT endpoints
# - Must be of type `int`
# - FastAPI will return a clear error if the type doesn't match

# ✅ Query Parameters:
# - `q` is an optional string query parameter in GET request
# - If you remove `= None`, it becomes required

# ✅ Request Body:
# - PUT request expects a JSON body that matches the `Item` model
# - Fields:
#     - `name` (str) - required
#     - `price` (float) - required
#     - `is_offer` (bool) - optional

# ✅ Features of FastAPI:
# - Automatically validates types and provides clear errors
# - Converts request/response bodies from/to JSON automatically
# - Auto-generates interactive docs (Swagger UI / ReDoc)
# - Enables client code generation in multiple languages
