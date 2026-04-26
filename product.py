from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from db import get_db

router = APIRouter()

# ✅ Schema (input validation)
class ProductCreate(BaseModel):
    name: str
    price: float


# ✅ ADD SINGLE PRODUCT (JSON body)
@router.post("/products")
def add_product(product: ProductCreate):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            (product.name, product.price)
        )
        db.commit()

        return {"msg": "Product added"}

    except Exception as e:
        return {"error": str(e)}


# ✅ BULK ADD PRODUCTS 🔥
@router.post("/products/bulk")
def add_bulk_products(products: List[ProductCreate]):
    try:
        db = get_db()
        cursor = db.cursor()

        for p in products:
            cursor.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s)",
                (p.name, p.price)
            )

        db.commit()

        return {
            "msg": "Bulk products added",
            "count": len(products)
        }

    except Exception as e:
        return {"error": str(e)}


# ✅ VIEW PRODUCTS
@router.get("/products")
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


# ✅ UPDATE PRODUCT (JSON body)
@router.put("/products/{id}")
def update_product(id: int, product: ProductCreate):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE products SET name=%s, price=%s WHERE id=%s",
        (product.name, product.price, id)
    )
    db.commit()

    return {"msg": "Product updated"}


# ✅ DELETE PRODUCT
@router.delete("/products/{id}")
def delete_product(id: int):
    db = get_db()
    cursor = db.cursor()

    # delete stock first
    cursor.execute("DELETE FROM stock WHERE product_id=%s", (id,))

    # delete product
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))

    db.commit()

    return {"msg": "Product deleted"}
