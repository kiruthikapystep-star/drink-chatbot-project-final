from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes import product, stock, order, chat

app = FastAPI()

# 🔥 CORS (frontend connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 API routes
app.include_router(product.router)
app.include_router(stock.router)
app.include_router(order.router)
app.include_router(chat.router)

# 🔥 Templates
templates = Jinja2Templates(directory="templates")

# 🔥 Chat UI (frontend)
@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔥 Admin UI
@app.get("/admin", response_class=HTMLResponse)
def admin_ui(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# 🔥 Home
@app.get("/")
def home():
    return {"message": "API working"}