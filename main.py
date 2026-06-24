import gradio as gr

from source.loaders import load_pdf

from source.chunks import recursive_chunks

from source.vectorstore import build_vectorstore,get_retriever

from source.chatbot import ask_pdf

retriever = None

def process_pdf(file):

    global retriever

    documents = load_pdf(file.name)

    chunks = recursive_chunks(documents)

    vectorstore = build_vectorstore(chunks)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5})

    return "PDF Processed Successfully"


def solve(query, history):

    global retriever

    if retriever is None:
        yield "⚠️ Please upload a PDF first."
        return

    yield from ask_pdf(query,history,retriever)


with gr.Blocks() as demo:

    gr.Markdown("# AI PDF Chatbot")

    file_upload = gr.File()

    process_btn = gr.Button("Process PDF")

    status = gr.Textbox()

    process_btn.click(process_pdf,inputs=file_upload,outputs=status)

    chatbot = gr.ChatInterface(fn=solve)

demo.launch()