# 📚 Chapter 10: Body - Nested Models
# FastAPI, powered by Pydantic, supports deeply nested and structured data using models, sets, lists, and even type-enforced dictionaries.

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

# ─────────────────────────────────────────────────────────────────────────────
# 🧺 List & Set Fields in Models

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []  # ⚠️ A generic list (no item type specified)
    distributors: set[str] = set()  # ✅ Set with specific string type

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

# 🧾 Example request body:
# {
#   "name": "Electric Guitar",
#   "description": "Solid body",
#   "price": 999.99,
#   "tax": 89.99,
#   "tags": ["music", "instrument"],
#   "distributors": ["yamaha", "gibson"]
# }

# ─────────────────────────────────────────────────────────────────────────────
# 🧱 Nested Models

class Image(BaseModel):
    url: str
    name: str

class ItemNested(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None  # 🪞 Nested Pydantic model

@app.put("/items_nested/{item_id}")
async def update_item(item_id: int, item: ItemNested):
    return {"item_id": item_id, "item": item}

# 🧾 Expected request body:
# {
#   "name": "Foo",
#   "description": "The pretender",
#   "price": 42.0,
#   "tax": 3.2,
#   "tags": ["rock", "metal", "bar"],
#   "image": {
#     "url": "http://example.com/baz.jpg",
#     "name": "The Foo live"
#   }
# }

# ─────────────────────────────────────────────────────────────────────────────
# 🌐 Special Types & Validation: HttpUrl

class ImageHttp(BaseModel):
    url: HttpUrl  # 🔐 Enforces URL validation
    name: str

class ItemHttp(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/items_http/{item_id}")
async def update_item(item_id: int, item: ItemHttp):
    return {"item_id": item_id, "item": item}

# 💡 Use of HttpUrl ensures that OpenAPI docs also reflect this validation.

# ─────────────────────────────────────────────────────────────────────────────
# 🧩 Arbitrary Dictionary Bodies

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

# 🧾 Expected request body:
# A JSON object where:
# • Keys must be integers
# • Values must be floats

# Example:
# {
#   "1": 0.25,
#   "2": 0.5,
#   "3": 0.25
#   "3.4": 5.0 # ⚠️ this will cause error: "Input should be a valid integer, unable to parse string as an integer"
# }

# 🔍 Important:
# Even though keys are defined as `int` in Python, JSON requires object keys to be strings.
# FastAPI will **automatically parse** keys like `"1"` into integers if defined as `dict[int, float]`.

# ─────────────────────────────────────────────────────────────────────────────
 