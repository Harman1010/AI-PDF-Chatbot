from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from source.loaders import load_pdf
from source.chunks import recursive_chunks
from source.vectorstore import build_vectorstore
from source.ocr import apply_ocr_if_needed

from backend import state

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    temp_path = f"temp_{file.filename}"

    try:

        # Save uploaded PDF
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Load PDF
        documents = load_pdf(temp_path)

        #documents = apply_ocr_if_needed(temp_path,documents)
        # Chunk documents
        chunks = recursive_chunks(documents)

        # Build vector store
        vectorstore = build_vectorstore(chunks)

        vectorstore.save_local("faiss_index")

        state.vectorstore = vectorstore

        return {
            "message": "PDF processed successfully."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)