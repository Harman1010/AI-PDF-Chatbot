from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Document
from backend.users import User
from backend.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/reset",
    tags=["Reset"]
)


@router.post("/")
def reset(session_id : str, db = Depends(get_db), current_user = Depends(get_current_user)):

    document = db.query(Document).filter(Document.session_id == session_id,Document.user_id == current_user.id).first()

    if document is None:
        raise HTTPException(status_code=404,detail="Document not found.")

    return {
        "message": "Conversation reset successfully."
    }