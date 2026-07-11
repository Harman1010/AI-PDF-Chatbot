from pathlib import Path

from langchain_community.vectorstores import FAISS

from source.embeddings import get_embeddings
from source.session import get_session_path


def load_vectorstore(session_id: str):

    session_path = get_session_path(session_id)

    if not session_path.exists():
        return None

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(session_path),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore