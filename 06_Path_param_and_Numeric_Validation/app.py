# 📘 Chapter 6: Path Parameters and Numeric Validations
# Just like we can use `Query` to declare validation and metadata for query parameters,
# we can use `Path` to do the same for path parameters.

from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

# ─────────────────────────────────────────────────────────

# 📍 Basic Path Parameter with Metadata

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],  # Title metadata shown in ReDoc and OpenAPI schema
    q: Annotated[str | None, Query(alias="item-query")] = None,       # Optional query param with alias
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 🔎 Note:
# - Path parameters are *always* required since they are part of the URL.
# - Even if you try setting a default or use `None`, it doesn't make them optional.

# ─────────────────────────────────────────────────────────

# 🔢 Numeric Validations using Path

@app.get("/items_nv/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],  # Enforces: item_id must be ≥ 1
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# ✅ Numeric constraints with `Path`:
# - `ge`: greater than or equal (>=)
# - `gt`: greater than (>)
# - `le`: less than or equal (<=)
# - `lt`: less than (<)
