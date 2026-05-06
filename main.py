from fastapi import FastAPI
from routes import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "AI Chatbot working 🚀"}
