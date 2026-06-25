from fastapi import APIRouter, HTTPException

from backend.schemas.chat import ChatRequest
from backend import state

from source.chatbot import ask_pdf

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest):

    if state.retriever is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first."
        )

    answer = ""

    for chunk in ask_pdf(
        request.query,
        [],
        state.retriever
    ):
        answer = chunk

    return {
        "answer": answer
    }