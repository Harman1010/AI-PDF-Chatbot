from fastapi import FastAPI

from backend.routers import upload,chat,reset

app = FastAPI()

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(reset.router)


@app.get("/")
def home():

    return {
        "message": "Welcome to AI PDF Chatbot API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }