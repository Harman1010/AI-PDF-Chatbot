import uuid
from pathlib import Path

BASE_DIR = Path("faiss_indexes")

def create_session()->str:
    """Creates session"""
    return str(uuid.uuid4())

def get_session_path(session_id:str)->Path:
    """Returns the directory where this id's faiss index is stored"""

    try:
        validate = uuid.UUID(session_id)

    except (ValueError, TypeError, AttributeError):
        raise ValueError("Invalid session ID") from None

    return BASE_DIR / str(validate)

def create_session_directory(session_id:str)->Path:
    """Creates the session's directory if it doesn't exist"""
    session_path = get_session_path(session_id)
    session_path.mkdir(parents=True,exist_ok=True)
    return session_path

