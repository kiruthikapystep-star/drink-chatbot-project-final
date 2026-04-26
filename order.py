from fastapi import APIRouter
from db import get_db

router = APIRouter()

@router.post("/order")
def place_order(name: str, qty: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE name=%s", (name,))
    product = cursor.fetchone()

    if not product:
        return {"message": "Product not found"}

    id, pname, price, stock = product

    if stock < qty:
        return {"message": "Not enough stock"}

    # reduce stock
    new_stock = stock - qty
    cursor.execute(
        "UPDATE products SET stock=%s WHERE id=%s",
        (new_stock, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Order placed",
        "remaining": new_stock
    }
