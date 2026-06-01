"""
SportRetail LAM — Mock API Server
Sirve los datos dummy como una REST API.

Uso:
    pip install fastapi uvicorn
    python api_server.py

Endpoints:
    GET /products          → todos los productos
    GET /products/{id}     → producto por id
    GET /products?category=Footwear&limit=10&skip=0
    GET /users             → todos los usuarios
    GET /users/{id}        → usuario por id
    GET /users?country=Colombia
    GET /carts             → todas las órdenes
    GET /carts/{id}        → orden por id
    GET /carts?userId=5&status=delivered
    GET /health            → health check
"""

import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="SportRetail LAM API",
    description="Mock API con datos wholesale de sportswear para LAM",
    version="1.0.0",
)

BASE = Path(__file__).parent

# ─── Load data at startup ───────────────────────────────────────────────────

def load(filename: str):
    with open(BASE / filename, encoding="utf-8") as f:
        return json.load(f)

PRODUCTS = load("products.json")["products"]
USERS    = load("users.json")["users"]
CARTS    = load("carts.json")["carts"]


# ─── Helpers ────────────────────────────────────────────────────────────────

def paginate(items: list, skip: int, limit: int):
    sliced = items[skip: skip + limit]
    return {"total": len(items), "skip": skip, "limit": limit, "count": len(sliced)}


# ─── Health ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "records": {
            "products": len(PRODUCTS),
            "users":    len(USERS),
            "carts":    len(CARTS),
        }
    }


# ─── Products ───────────────────────────────────────────────────────────────

@app.get("/products")
def get_products(
    limit:    int            = Query(default=30,  ge=1, le=200),
    skip:     int            = Query(default=0,   ge=0),
    category: Optional[str] = Query(default=None),
    brand:    Optional[str] = Query(default=None),
):
    items = PRODUCTS
    if category:
        items = [p for p in items if p["category"].lower() == category.lower()]
    if brand:
        items = [p for p in items if p["brand"].lower() == brand.lower()]

    meta = paginate(items, skip, limit)
    return {**meta, "products": items[skip: skip + limit]}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")


@app.get("/products/categories/list")
def get_categories():
    cats = sorted(set(p["category"] for p in PRODUCTS))
    return {"categories": cats}


# ─── Users ──────────────────────────────────────────────────────────────────

@app.get("/users")
def get_users(
    limit:         int            = Query(default=30,  ge=1, le=200),
    skip:          int            = Query(default=0,   ge=0),
    country:       Optional[str] = Query(default=None),
    retailerType:  Optional[str] = Query(default=None),
):
    items = USERS
    if country:
        items = [u for u in items if u["country"].lower() == country.lower()]
    if retailerType:
        items = [u for u in items if u["retailerType"].lower() == retailerType.lower()]

    meta = paginate(items, skip, limit)
    return {**meta, "users": items[skip: skip + limit]}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for u in USERS:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.get("/users/{user_id}/carts")
def get_user_carts(user_id: int):
    user_carts = [c for c in CARTS if c["userId"] == user_id]
    if not user_carts:
        raise HTTPException(status_code=404, detail=f"No carts found for user {user_id}")
    return {"userId": user_id, "total": len(user_carts), "carts": user_carts}


# ─── Carts / Orders ─────────────────────────────────────────────────────────

@app.get("/carts")
def get_carts(
    limit:   int            = Query(default=30,  ge=1, le=300),
    skip:    int            = Query(default=0,   ge=0),
    userId:  Optional[int] = Query(default=None),
    status:  Optional[str] = Query(default=None),
    channel: Optional[str] = Query(default=None),
):
    items = CARTS
    if userId:
        items = [c for c in items if c["userId"] == userId]
    if status:
        items = [c for c in items if c["status"].lower() == status.lower()]
    if channel:
        items = [c for c in items if c["channel"].lower() == channel.lower()]

    meta = paginate(items, skip, limit)
    return {**meta, "carts": items[skip: skip + limit]}


@app.get("/carts/{cart_id}")
def get_cart(cart_id: int):
    for c in CARTS:
        if c["id"] == cart_id:
            return c
    raise HTTPException(status_code=404, detail=f"Cart {cart_id} not found")


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
