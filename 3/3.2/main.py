from fastapi import FastAPI, HTTPException
from typing import Optional, List

app = FastAPI()

sample_products = [
  {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
  },
  {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
  },
  {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
  },
  {
    "product_id": 101,
    "name": "Headphones",
    "category": "Electronics",
    "price": 199.99
  },
  {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
  }
]

@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/search")
def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: int = 10
):
    results = []

    for product in sample_products:
        if keyword.lower() in product["name"].lower():

            if category is None or product["category"].lower() == category.lower():
                results.append(product)
                
    return results[:limit]

@app.get("/products")
def get_products():
    return sample_products

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    for i, product in enumerate(sample_products):
        if product["product_id"] == product_id:
            delete_product = sample_products.pop(i)
            return {
                "massage": "Product deleted",
                "product": delete_product
            }
        
    raise HTTPException(status_code=404, detail="Product not found")