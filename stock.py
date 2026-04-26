from fastapi import APIRouter
from db import get_db

router = APIRouter()

@router.post("/stock")
def update_stock(data: dict):
    conn = get_db()
    cursor = conn.cursor()

    product_id = data["product_id"]
    quantity = int(data["quantity"])

    # 🔥 UPDATE DIRECTLY IN PRODUCTS TABLE
    cursor.execute(
        "UPDATE products SET stock=%s WHERE id=%s",
        (quantity, product_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    if quantity < 5:
        return {"msg": "Low stock warning ⚠️"}

    return {"msg": "Stock updated ✅"}
