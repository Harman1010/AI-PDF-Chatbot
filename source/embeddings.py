from langchain_huggingface import HuggingFaceEmbeddings
from source.config import EMBEDDING_MODEL

_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def get_embeddings():
    
    return _embeddings