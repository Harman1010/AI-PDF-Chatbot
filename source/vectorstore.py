from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from source.config import EMBEDDING_MODEL,TOP_K
from source.embeddings import get_embeddings


def build_vectorstore(chunks):

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore