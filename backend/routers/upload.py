from sqlalchemy.orm import Session
from fastapi import Depends

from backend.auth_dependencies import get_current_user
from backend.database import get_db
from backend.models import Document
from backend.users import User

from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import tempfile
import shutil

from source.loaders import load_pdf
from source.chunks import recursive_chunks
from source.vectorstore import build_vectorstore

from source.session import create_session,create_session_directory

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...),db : Session = Depends(get_db),current_user = Depends(get_current_user)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    temp_path = None

    session_path = None

    MAX_LIMIT = 10 * 1024 * 1024
    CHUNK_SIZE = 1024 * 1024

    try:
         # Save uploaded PDF
        with tempfile.NamedTemporaryFile(mode="wb",suffix=".pdf",delete=False) as buffer:
            temp_path = buffer.name
            total_size = 0

            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_LIMIT:
                    raise HTTPException(
                        status_code=413,
                        detail="PDF exceeds the 10 MB upload limit."
                    )

                buffer.write(chunk)

        with open(temp_path, "rb") as pdf_file:
            file_signature = pdf_file.read(5)

            if file_signature != b"%PDF-":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid PDF file."
                )

        # Load PDF
        documents = load_pdf(temp_path)

        #documents = apply_ocr_if_needed(temp_path,documents)
        # Chunk documents
        chunks = recursive_chunks(documents)

        session_id = create_session()

        session_path = create_session_directory(session_id)

        vectorstore = build_vectorstore(chunks)

        vectorstore.save_local(str(session_path))

        document = Document(user_id = current_user.id,filename=file.filename,session_id=session_id,status="ready")

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "message" : "PDF processed successfully!",
            "session_id" : session_id
        }

    except HTTPException:

        db.rollback()
        
        if session_path and session_path.exists():
            shutil.rmtree(session_path)
        raise

    except Exception as e:

        db.rollback()

        if session_path and session_path.exists():
            shutil.rmtree(session_path)

        raise HTTPException(
            status_code=500,
            detail="Error processing PDF")

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()