from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from source.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def recursive_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(documents)