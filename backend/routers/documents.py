from backend.auth_dependencies import get_current_user

from backend.database import get_db

from backend.models import Document

from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

import shutil

from fastapi import Path as PathParam
from source.session import get_session_path

router = APIRouter()

@router.get("/documents")

def get_documents(db : Session = Depends(get_db),curr_user = Depends(get_current_user)):

    documents =  db.query(Document).filter(Document.user_id == curr_user.id).all()

    if not documents:

        raise HTTPException(status_code=404,detail="No document associated with this user")

    return [
        {
            "session_id": doc.session_id,
            "filename": doc.filename,
            "created_at": doc.created_at,
            "status": doc.status
        }
        for doc in documents
    ]

@router.delete("/documents/{session_id}")
def remove_document(session_id : str , db : Session = Depends(get_db), curr_user = Depends(get_current_user)):

    document = db.query(Document).filter(Document.session_id == session_id, Document.user_id == curr_user.id).first()

    if document is None:

        raise HTTPException(status_code=404,detail="No documents associated with this user")

    session_path = get_session_path(session_id)

    if session_path.exists():
        shutil.rmtree(session_path)



