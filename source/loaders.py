from langchain_community.document_loaders import PyPDFLoader

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text.strip()

def load_pdf(file_path):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    return documents