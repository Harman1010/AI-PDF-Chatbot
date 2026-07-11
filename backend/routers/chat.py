from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.schemas.chat import ChatRequest

from source.vectorLoader import load_vectorstore

from source.chatbot import ask_pdf


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest):

    vectorstore = load_vectorstore(request.session_id)

    if vectorstore is None:
        raise HTTPException(status_code=404,detail="Unable to find active session. Please upload a document")

    return StreamingResponse(
        ask_pdf(
            request.query,
            request.history,
            vectorstore
        ),
        media_type="text/plain"
    )