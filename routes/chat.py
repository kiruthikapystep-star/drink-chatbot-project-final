from fastapi import APIRouter
from db import get_db

router = APIRouter()

@router.get("/chat")
def chat(message: str):
    conn = get_db()

    if conn is None:
        return {"reply": "DB connection failed ❌"}

    cursor = conn.cursor()
    message = message.lower().strip()

    # 🔥 ORDER COMMAND FIRST
    if message.startswith("order"):
        parts = message.split()

        if len(parts) >= 2:
            pname = parts[1]

            cursor.execute(
                "SELECT * FROM products WHERE LOWER(name)=LOWER(%s)",
                (pname,)
            )
            product = cursor.fetchone()

            if product:
                id, name, price, stock = product

                if stock > 0:
                    cursor.execute(
                        "UPDATE products SET stock=%s WHERE id=%s",
                        (stock - 1, id)
                    )
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return {
                        "reply": f"Order confirmed ✅ {name} | Price ₹{price}"
                    }
                else:
                    cursor.close()
                    conn.close()
                    return {"reply": f"{name} out of stock ❌"}

            else:
                cursor.close()
                conn.close()
                return {"reply": "Product not found 😕"}

    # 🔥 NORMAL PRODUCT CHECK
    cursor.execute(
        "SELECT * FROM products WHERE LOWER(name)=LOWER(%s)",
        (message,)
    )
    product = cursor.fetchone()

    if product:
        id, name, price, stock = product

        if stock > 0:

            # 🔥 LOW STOCK CHECK
            if stock < 5:
                reply = f"Only {stock} left ⚠️ Hurry! Price ₹{price}"
            else:
                reply = f"{name} available 👍 Price ₹{price}"

            reply += f". Type 'order {name}' to buy"

        else:
            reply = f"{name} out of stock ❌"

    else:
        cursor.execute("SELECT name FROM products")
        products = cursor.fetchall()

        suggestions = [p[0] for p in products]

        cursor.close()
        conn.close()

        return {
            "reply": "Product not found 😕",
            "suggestions": suggestions
    }

    cursor.close()
    conn.close()

    return {"reply": reply}
