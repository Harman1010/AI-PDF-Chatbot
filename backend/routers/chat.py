from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.schemas.chat import ChatRequest
from backend import state

from source.chatbot import ask_pdf


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest):

    if state.vectorstore is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first."
        )

    return StreamingResponse(
        ask_pdf(
            request.query,
            request.history,
            state.vectorstore
        ),
        media_type="text/plain"
    )