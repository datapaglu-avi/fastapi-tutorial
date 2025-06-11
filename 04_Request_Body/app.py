# Chapter 4 → Request Body
# Explains how to receive and validate request body data in FastAPI using Pydantic models.
# A request body is data sent by the client to your API. A response body is the data your API sends to the client.

from fastapi import FastAPI
from pydantic import BaseModel

# ───────────────────────────────────────────────
# ✅ Declare the Request Body using Pydantic
# ───────────────────────────────────────────────

# Define a data model using a class that inherits from Pydantic's BaseModel
class Item(BaseModel):
    name: str                    # Required
    description: str | None = None  # Optional → default = None
    price: float                 # Required
    tax: float | None = None     # Optional

# When a field has a default value (or is set to None), it becomes optional

app = FastAPI()


# ───────────────────────────────────────────────
# ✅ POST Request with Body
# ───────────────────────────────────────────────

@app.post("/items/")
async def create_item(item: Item):
    # The parameter `item` will automatically receive, parse and validate the request body as an `Item` object
    return item

# ✅ What FastAPI does for you:
# - Reads the body of the request as JSON
# - Converts types (e.g. strings to floats if possible)
# - Validates required and optional fields
# - Returns detailed error messages if validation fails
# - Automatically shows model structure in Swagger UI (/docs)
# - Generates JSON Schema + OpenAPI definitions

# Example request:
# POST /items/
# {
#     "name": "Laptop",
#     "description": "Gaming laptop",
#     "price": 1099.99,
#     "tax": 199.99
# }


# ───────────────────────────────────────────────
# ✅ PUT Request → Request Body + Path + Query Param
# ───────────────────────────────────────────────

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    # item_id → taken from the URL path
    # item → parsed from request body
    # q → optional query parameter
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# Recognition logic:
# - If param in path → treated as path parameter
# - If simple type (int, str, bool) → treated as query parameter
# - If BaseModel → treated as request body

# Example:
# PUT /items/7?q=note
# Body:
# {
#     "name": "Notebook",
#     "description": "Lined pages",
#     "price": 99.99,
#     "tax": 5.0
# }

# Response:
# {
#     "item_id": 7,
#     "name": "Notebook",
#     "description": "Lined pages",
#     "price": 99.99,
#     "tax": 5.0,
#     "q": "note"
# }

# ⚠️ GET requests generally shouldn’t have a body
# → Swagger UI doesn’t render body input for GET
# → Some HTTP proxies and clients may strip it
