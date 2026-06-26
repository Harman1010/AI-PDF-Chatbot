from fastapi import FastAPI

from backend.routers import upload,chat,reset

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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