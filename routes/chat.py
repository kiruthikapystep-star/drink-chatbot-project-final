from fastapi import APIRouter
from db import get_db

router = APIRouter()

@router.get("/chat")
def chat(message: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM products")
    products = cursor.fetchall()

    message = message.lower()

    # 🔹 intent detection
    if "price" in message or "cost" in message:
        for name, price in products:
            if name.lower() in message:
                return {"reply": f"{name} costs ₹{price}"}

    if "available" in message or "have" in message:
        for name, price in products:
            if name.lower() in message:
                return {"reply": f"Yes, {name} is available for ₹{price}"}

    # 🔹 recommendation
    if "suggest" in message or "recommend" in message:
        name, price = products[0]
        return {"reply": f"You can try {name} for ₹{price}"}

    # 🔹 fallback search
    for name, price in products:
        if name.lower() in message:
            return {"reply": f"{name} available for ₹{price}"}

    return {"reply": "Sorry, I couldn’t find that product"}
