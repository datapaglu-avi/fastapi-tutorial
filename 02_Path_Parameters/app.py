# Chapter 2 → Path Parameters
# Covers how to use dynamic values in URLs, and how to validate and restrict them.

from fastapi import FastAPI # type: ignore
from enum import Enum

app = FastAPI()

# ───────────────────────────────────────────────
# ✅ Basic Path Parameter
# ───────────────────────────────────────────────

@app.get("/items/{item_id}")
async def read_item(item_id):
    # `item_id` is captured from the path and passed to this function
    return {"item_id": item_id}
    # Example: GET /items/5 → {"item_id": "5"}
    # Note: Without type hints, item_id will be treated as a string


# ───────────────────────────────────────────────
# ✅ Path Parameters with Types
# ───────────────────────────────────────────────

@app.get("/typed-items/{item_id}")
async def read_item_typed(item_id: int):
    return {"item_id": item_id}
    # item_id is explicitly expected to be an integer
    # Example: GET /typed-items/3 → {"item_id": 3}
    # Passing a non-int like "three" → 422 Unprocessable Entity + clear error in docs


# ───────────────────────────────────────────────
# ✅ Order Matters for Path Operations
# ───────────────────────────────────────────────

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
    # NOTE: /users/me must be declared **before** /users/{user_id}
    # Otherwise, the word "me" will be captured as user_id and handled by the second route


# ───────────────────────────────────────────────
# ⚠️ Path Redefinition is Not Allowed
# ───────────────────────────────────────────────

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

# This second definition will never be used and should be avoided
# @app.get("/users")
# async def read_users2():
#     return ["Bean", "Elfo"]


# ───────────────────────────────────────────────
# ✅ Restrict Path Values using Enum
# ───────────────────────────────────────────────

class ItemID(str, Enum):
    item_1 = "item_1"
    item_2 = "item_2"
    item_3 = "item_3"

@app.get("/items-enum/{item_id}")
async def get_model(item_id: ItemID):
    if item_id == ItemID.item_1:
        return {"item_id": item_id, "message": "item_1"}

    if item_id.value in ["item_1", "item_2", "item_3"]:
        return {"item_id": item_id, "message": "valid item"}

    return {"item_id": item_id, "message": "Not a valid item"}

# This limits acceptable values to: item_1, item_2, item_3
# Swagger docs will show a dropdown selector
# Invalid values → 422 error: "Input should be 'item_1', 'item_2' or 'item_3'"


# ───────────────────────────────────────────────
# ✅ Path Parameters That Contain Paths
# ───────────────────────────────────────────────

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
    # `:path` makes the parameter accept slashes
    # Example: GET /files/folder/subfolder/file.txt → {"file_path": "folder/subfolder/file.txt"}
