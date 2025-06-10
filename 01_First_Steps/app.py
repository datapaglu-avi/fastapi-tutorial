# Chapter 1 → First Steps
# This is the simplest working FastAPI app, explained step by step.

from fastapi import FastAPI  # type: ignore
# 📌 FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.
# It’s built on top of Starlette (for the web parts) and Pydantic (for data validation).

# ─────────────────────────────
# ✅ Create a FastAPI App Instance
# ─────────────────────────────
app = FastAPI()
# This creates the core app object, which holds all your routes and settings.

# ─────────────────────────────
# ✅ Define a Path Operation (aka Route)
# ─────────────────────────────
@app.get("/")
# This decorator tells FastAPI to run the function below when:
# - The path is "/" (root of the site)
# - The HTTP method is GET

# "Path" = endpoint or route (everything after the domain, e.g., /users, /posts)
# "Operation" = HTTP method (GET, POST, PUT, DELETE, etc.)

async def root():
    # This function will run whenever someone sends a GET request to "/"
    # `async` allows for asynchronous handling (e.g., DB or network operations)
    return {"message": "Hello World"}
    # FastAPI automatically converts this dict into a JSON response:
    # → { "message": "Hello World" }

# ─────────────────────────────
# 🛠️ How to Run This App
# ─────────────────────────────

# Using `fastapi dev` (a development runner similar to Flask's debug mode):
# Run in terminal:
#     fastapi dev 01_First_Steps/app.py
#
# Output will include something like:
#     INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
#
# Now open:
#     http://127.0.0.1:8000           → to test the API
#     http://127.0.0.1:8000/docs      → interactive Swagger docs
#     http://127.0.0.1:8000/redoc     → alternative ReDoc docs

# ─────────────────────────────
# 📚 HTTP Method Reference
# ─────────────────────────────
# The main HTTP methods you’ll use in an API:

# GET     → Read data (e.g., fetch an item)
# POST    → Create new data (e.g., submit a form)
# PUT     → Update an entire item
# PATCH   → Update part of an item
# DELETE  → Delete an item
# OPTIONS / HEAD / TRACE → Less common, used for metadata or debugging

# Summary:
# - @app.get("/") defines a GET route for the root URL
# - root() handles that request and returns a JSON response
# - This is the absolute minimum you need to create an API in FastAPI
