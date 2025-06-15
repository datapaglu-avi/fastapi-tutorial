# 📚 Chapter 09: Body - Fields
# Learn how to add validations and metadata *inside* Pydantic models using `Field`, 
# similar to how we use `Query`, `Path`, and `Body` in function parameters.

from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field  # 🧱 Import Field to define metadata in models

app = FastAPI()

# ─────────────────────────────────────────────────────────────────────────────
# 🧰 Using Field for Validation and Metadata in Pydantic Models

class Item(BaseModel):
    name: str

    # 📝 Adds metadata like title and restricts max length
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )

    # 💰 Adds a validation rule: price must be greater than 0
    price: float = Field(
        gt=0,
        description="The price must be greater than zero"
    )

    # 🌐 No extra metadata, just a regular optional float
    tax: float | None = None

# ─────────────────────────────────────────────────────────────────────────────
# 📤 Using Field-enhanced Models in Request Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[Item, Body(embed=True)]  # Embeds the `item` under its key in the body
):
    """
    Endpoint demonstrating how to receive a Pydantic model with internal Field-level
    validation and metadata.
    """
    results = {"item_id": item_id, "item": item}
    return results

# 🧾 Sample Request Body:
# {
#     "item": {
#         "name": "Acoustic Guitar",
#         "description": "A beautifully crafted 6-string guitar",
#         "price": 499.99,
#         "tax": 49.99
#     }
# }

# ─────────────────────────────────────────────────────────────────────────────
# 🧠 Note:
# `Field` works just like `Query`, `Path`, and `Body`, and accepts similar parameters:
# - `default`, `title`, `description`, `gt`, `lt`, `max_length`, etc.
# It's ideal for encapsulating validations *within* the model definition itself.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 🧠 Note:
# ✅ FastAPI enforces parameter types at different stages:
# 
# • If `item_id` is given as a float (e.g., 12.5 instead of an integer),
#   ➤ The request is **rejected by the OpenAPI schema**, and you won't be able to make the PUT call at all.
#
# • If `item.price` is negative (e.g., -10.0),
#   ➤ The request will go through, but FastAPI will **return a 422 Unprocessable Entity**
#     response due to Pydantic validation failing on the `gt=0` constraint.
# 
# This shows how type validation and schema validation work together:
# - Path/query validations (like `item_id: int`) are enforced at the request parsing stage
# - Body model validations (via `Field(...)`) are enforced after the request is accepted

# 🔍 Why This Happens:
# - Path/Query parameters: Validated at the routing and OpenAPI schema level. They're strict — wrong types = rejected before processing.
# - Body parameters: Parsed into Pydantic models. Validation errors here raise a 422 error after the request is technically "received".
# ─────────────────────────────────────────────────────────────────────────────
