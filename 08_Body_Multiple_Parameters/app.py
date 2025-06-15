# 📚 Chapter 08: Body - Multiple Parameters
# Learn how to combine Path, Query, and Body parameters effectively in FastAPI,
# and how FastAPI handles multiple body inputs.

from typing import Annotated
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()

# ─────────────────────────────────────────────────────────────────────────────
# 📦 Defining a Pydantic model for item
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# ─────────────────────────────────────────────────────────────────────────────
# 🔀 Mixing Path, Query, and Body Parameters

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None  # Optional body parameter
):
    """
    This endpoint demonstrates how to combine:
    - Path parameters (item_id)
    - Query parameters (q)
    - Body parameters (item)
    
    If a body is provided, it should match the structure of the Item model.
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# 🧾 Expected JSON body for `item`:
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }

# ─────────────────────────────────────────────────────────────────────────────
# 👥 Handling Multiple Body Parameters

# Additional model for user data
class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items_multiple/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    """
    Demonstrates multiple body parameters being received and parsed.
    FastAPI expects a JSON object with top-level keys matching the parameter names: `item` and `user`.
    """
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# 🧾 Expected JSON body:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }

# 💡 Tip:
# To achieve similar nested key behavior for optional body parameters,
# use `Body(embed=True)`:
# item: Annotated[Item | None, Body(embed=True)] = None

# ─────────────────────────────────────────────────────────────────────────────
# 🔢 Using Singular Values in the Request Body

@app.put("/items_singular_item/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()]  # Required to treat `importance` as a body parameter
):
    """
    FastAPI treats singular values like `int`, `str` as query params by default.
    Use Body() to explicitly mark them as body fields.
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# 🧾 Expected JSON body:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }

# ─────────────────────────────────────────────────────────────────────────────
