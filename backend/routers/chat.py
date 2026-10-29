from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.schemas.chat import ChatRequest

from source.vectorLoader import load_vectorstore

from source.chatbot import ask_pdf

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Document


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest,db : Session = Depends(get_db)):

    document = db.query(Document).filter(Document.session_id == request.session_id).first()

    if document is None:

        raise HTTPException(status_code=404,detail="Document not found. Please upload a document")

    if document.status != "ready":
        raise HTTPException(status_code=409,detail="Document is not ready for chatting")


    try:
        vectorstore = load_vectorstore(request.session_id)

    except ValueError:

        raise HTTPException(status_code=400,detail="Invalid session ID") from None

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