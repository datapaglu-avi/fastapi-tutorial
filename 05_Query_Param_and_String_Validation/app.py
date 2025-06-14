# 📘 Chapter 5: Query Parameters and String Validations
# FastAPI lets us define extra metadata and validation rules for query parameters.

from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

# ─────────────────────────────────────────────────────────

# 🎯 Optional Query Parameters

@app.get("/items/")
# The query parameter `q` is of type str | None, meaning it can either be a string or None.
# Since the default value is None, FastAPI considers it optional.
# Using `str | None` helps editors with better autocomplete and type checking.
# Any default value (even None) makes a parameter optional.
async def read_items(q: str | None = None): 
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# ─────────────────────────────────────────────────────────

# 🔒 Validating Query Length

@app.get("/items_50/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    # Although optional, if `q` is provided, it must not exceed 50 characters.
    # We're using `Query()` since this is a query parameter.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# FastAPI will:
# ✅ Enforce the max length
# 🚨 Raise a clear error if violated
# 📄 Document the constraint in OpenAPI (auto docs)

# ─────────────────────────────────────────────────────────

# 🔍 Regex and Length Validation

@app.get("/items_regex/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    # `q` must be 3–50 characters long and exactly match "fixedquery"
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# ─────────────────────────────────────────────────────────

# 📦 List of Query Parameters

@app.get("/items_list/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    # Accepts multiple values: ?q=foo&q=bar
    # Use `Query()` to explicitly tell FastAPI it's a query param (not request body).
    query_items = {"q": q}
    return query_items

# ─────────────────────────────────────────────────────────

# 🏷️ Adding Metadata

@app.get("/items_additional_meta/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string title",  # Visible in ReDoc, not Swagger UI
            description="Search query for matching items in the database",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# ─────────────────────────────────────────────────────────

# 🧪 Parameter Aliases

@app.get("/items_alias/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    # Lets you use a non-Python-compatible name like "item-query" in the URL.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# ─────────────────────────────────────────────────────────

# ⚠️ Deprecating Query Parameters

@app.get("/items_deprecated/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Search query for matching items in the database",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,  # Will show as deprecated in the docs
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# ─────────────────────────────────────────────────────────

# 🕵️ Hiding Parameters from Docs

@app.get("/items_exclude/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    # `hidden_query` won't appear in OpenAPI schema or docs
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

# ─────────────────────────────────────────────────────────

# 🧰 Custom Validation Example with AfterValidator (Pydantic)

# Example syntax:
# id: Annotated[str | None, AfterValidator(check_valid_id)] = None
# def check_valid_id(id: str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError('Invalid ID format, must start with "isbn-" or "imdb-"')
#     return id
