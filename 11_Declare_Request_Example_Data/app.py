# 📘 Chapter 11: Declare Request Example Data
# FastAPI allows you to document example request bodies to improve your OpenAPI docs and help users understand what kind of data to send.

from typing import Annotated
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

# ─────────────────────────────────────────────────────────────────────────────
# 📦 Model-Level Example with `json_schema_extra`

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # ✅ This adds example data to the schema which shows up in the Swagger docs.
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

# ─────────────────────────────────────────────────────────────────────────────
# 🧾 Field-Level Examples Using `Field()`

class User(BaseModel):
    name: str = Field(examples=["Avi Kasliwal"])
    occupation: str | None = Field(default=None, examples=["Data Engineer"])

@app.put("/items_field/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}

# 👆 Each field in the Pydantic model can have its own sample value shown in Swagger UI.

# ─────────────────────────────────────────────────────────────────────────────
# 📚 Declaring Multiple Examples with `examples` in `Body()`

@app.put("/items_body/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",  # Will be automatically converted to float
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",  # ❌ Invalid - will trigger validation error
                },
            ],
        ),
    ],
):
    return {"item_id": item_id, "item": item}

# 🧠 Note: These examples are added to the JSON Schema, but Swagger UI does not display multiple examples directly.

# ─────────────────────────────────────────────────────────────────────────────
# 🛠️ Using `openapi_examples` for More Customization

@app.put("/items_openapi/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",  # ❌ Will cause 422 error
                    },
                },
            },
        ),
    ],
):
    return {"item_id": item_id, "item": item}

# ✅ With `openapi_examples`, you get:
# - A key name for each example (e.g., "normal", "converted")
# - A summary and description (supports Markdown!)
# - Example data (or external URL via `externalValue`)

# 🔥 Swagger UI renders these examples more cleanly than plain `examples=[]`.

# ─────────────────────────────────────────────────────────────────────────────
