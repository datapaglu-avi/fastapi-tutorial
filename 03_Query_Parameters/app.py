# Chapter 3 → Query Parameters
# Covers how to use query parameters in FastAPI, including optional/required ones, type conversions, and combinations with path params.

from fastapi import FastAPI #type: ignore

app = FastAPI()

# ───────────────────────────────────────────────
# ✅ Basic Query Parameters
# ───────────────────────────────────────────────

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    # Query params are passed like: /items/?skip=0&limit=10
    return fake_items_db[skip : skip + limit]

# Query = key-value pairs in the URL after "?" → separated by "&"
# By default, all non-path parameters in the function are treated as query parameters
# Example: /items/?skip=1&limit=2 → returns 2 items starting from index 1
# Type validation:
# /items/?skip=avi → error: "Value must be an integer"


# ───────────────────────────────────────────────
# ✅ Optional Query Parameters
# ───────────────────────────────────────────────

@app.get("/items/{item_id}")
async def read_item_optional_q(item_id: str, q: str | None = None):
    # `q` is optional → will default to None if not provided
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# FastAPI will automatically detect:
# - `item_id` as a path parameter
# - `q` as a query parameter


# ───────────────────────────────────────────────
# ✅ Multiple Path + Query Parameters
# ───────────────────────────────────────────────

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    q: str | None = None,
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description": "This is an amazing item that has a long description"
        })
    return item

# Example:
# /users/1/items/abc?q=hello&short=true
# → returns: {"item_id": "abc", "owner_id": 1, "q": "hello"}
# If short=false or not provided, long description will be included


# ───────────────────────────────────────────────
# ✅ Required Query Parameters
# ───────────────────────────────────────────────

@app.get("/items_required/{item_id}")
async def read_user_item_required(item_id: str, needy: str):
    # `needy` has no default value → required query param
    return {"item_id": item_id, "needy": needy}

# /items_required/xyz?needy=hello → works
# /items_required/xyz → returns 422 Unprocessable Entity
# Error will include: "msg": "Field required", "loc": ["query", "needy"]


# ───────────────────────────────────────────────
# ✅ Mixing Required, Optional, and Default Query Params
# ───────────────────────────────────────────────

@app.get("/items_mix_n_match/{item_id}")
async def read_user_item_mix(
    item_id: str,
    needy: str,                     # required
    skip: int = 0,                  # default → optional
    limit: int | None = None        # optional
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# Example:
# /items_mix_n_match/x23?needy=yes&skip=5&limit=10
# → returns all parameters
#
# /items_mix_n_match/x23?needy=yes
# → works with default skip=0 and limit=None
#
# /items_mix_n_match/x23
# → ❌ returns 422 due to missing `needy`
