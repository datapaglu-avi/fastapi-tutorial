# 📘 Chapter 07: Query Parameter Models
# When multiple query parameters are conceptually related,
# it's better to group them into a Pydantic model for clarity, reuse, and validation. 😎

from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ─────────────────────────────────────────────────────────

# 📦 Define Query Parameter Model

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # ⛔ Forbid unknown/extra query params (useful in strict APIs)

    limit: int = Field(100, gt=0, le=100)  # ✅ Default = 100, must be 1–100
    offset: int = Field(0, ge=0)          # ✅ Must be ≥ 0
    order_by: Literal["created_at", "updated_at"] = "created_at"  # 🔁 Enum-style fixed options
    tags: list[str] = []                 # 🏷️ Multiple string values (e.g. ?tags=foo&tags=bar)

# ─────────────────────────────────────────────────────────

# 🚀 Use Query Parameter Model in Endpoint

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    # FastAPI extracts query parameters into `filter_query` using the FilterParams model.
    return filter_query

# ─────────────────────────────────────────────────────────

# 🧪 Sample Request (cURL):
# curl -X 'GET' \
#   'http://127.0.0.1:8000/items/?limit=5&offset=1&order_by=updated_at&tags=kak&tags=ojfmirkn' \
#   -H 'accept: application/json'

# 🛑 If any unknown query parameter is passed, FastAPI will return:
# {
#   "detail": [{"type": "extra_forbidden", "msg": "Extra inputs are not permitted", ... }]
# }
