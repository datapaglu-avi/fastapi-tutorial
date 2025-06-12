from fastapi import FastAPI # type: ignore
from pydantic import BaseModel, Field # type: ignore


class Review(BaseModel):
    reviewer: str = 'Anonymous'
    rating: float = Field(ge = 0.0, le = 5.0)
    comment: str


class Product(BaseModel):
    id: int | None = None
    name: str                    
    description: str | None = None  
    price: float = Field(gt = 0.0)                
    in_stock: float | None = None
    reviews: list[Review] = []


products: Product = []

app = FastAPI()


@app.post('/products')
async def product(product: Product):
    id = len(products) + 1
    if product not in products:
        product.id = id
        products.append(product)
        return {
            'msg': 'Product added',
            'products': products
        }
    else:
        return {
            'msg': 'Product already present in the database',
            'product': product
        }
    

@app.get('/products/{product_id}')
async def product(product_id: int):
    for product in products:
        if product.id == product_id:
            return {
                'product': product
            }
    return {
        'msg': f'No product found with id {product_id}'
    }


@app.get('/products')
async def enlist_products(skip: int = 0, limit: int = 10):
    return {
        'products': products[skip: skip + limit]
    }


@app.put('/products/{product_id}/reviews')
async def review(product_id: int, review: Review):
    for product in products:
        if product.id == product_id:
            product.reviews.append(review)
            return {
                'product': product
            }
    return {
        'msg': f'No product found with id {product_id}'
    }


@app.get('/products/{product_id}/reviews')
async def reviews(product_id: int, min_rating: float | None = None):
    for product in products:
        if product.id == product_id:
            if min_rating is not None:
                return {
                    'reviews': [r for r in product.reviews if r.rating >= min_rating]
                }
            else:
                return {
                    'reviews': product.reviews
                }
    return {
        'msg': f'No product found with id {product_id}'
    }
        

@app.delete('/products/{product_id}')
async def delete(product_id: int):
    global products
    products = [p for p in products if p.id != product_id]

# TEST ITEMS ADDED VIA POST PATH OPERATION

# curl -X 'POST' \
#   'http://127.0.0.1:8000/products' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "id": 0,
#   "name": "Chips",
#   "description": "Crispy potato chips",
#   "price": 50,
#   "in_stock": 5
# }'

# curl -X 'POST' \
#   'http://127.0.0.1:8000/products' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "id": 0,
#   "name": "Chocolates",
#   "description": "Milk Chocolate",
#   "price": 5,
#   "in_stock": 45
# }'