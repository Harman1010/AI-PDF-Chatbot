# AI PDF Chatbot

This project is a simple AI chatbot that can read a PDF and answer questions based on its content. The idea was to understand how Retrieval-Augmented Generation (RAG) systems work in practice.

---

## What it does

* Takes a PDF as input
* Extracts text from it
* Breaks the text into smaller parts
* Finds the most relevant parts when a question is asked
* Uses a language model to generate an answer

---

## How it works

First, the PDF is loaded and text is extracted. That text is then split into chunks (with a bit of overlap so context isn’t lost).

Each chunk is converted into embeddings using a sentence transformer model, and those embeddings are stored in FAISS.

When a user asks a question, the system converts the query into an embedding and searches for the most similar chunks. These chunks are then passed to a language model, which generates the final answer.

In some cases, if the context is not enough, the model can still answer using general knowledge.

---

## Tech stack

* Python
* SentenceTransformers
* FAISS
* Hugging Face Transformers (FLAN-T5)
* LangChain
* Gradio

---

## What I learned

* How RAG systems combine retrieval + generation
* Why chunking strategy matters a lot
* How embeddings and vector search work
* Difference between building everything manually vs using LangChain

---

## Limitations

* Retrieval is not always perfect
* Sometimes the answer is incomplete or slightly off
* Depends heavily on how text is chunked
* The model (FLAN-T5) is not very strong compared to newer LLMs

---

## Future improvements

* Better chunking (sentence/semantic-based)
* Add reranking for more accurate retrieval
* Use a stronger LLM
* Improve UI and support multiple PDFs

---

## Notes

I built two versions of this project:

* One from scratch (manual pipeline)
* One using LangChain

This helped me understand both low-level and high-level approaches.

---



## Final thoughts

This project was mainly for learning how real-world AI systems handle documents and queries. It gave me a good understanding of embeddings, vector databases, and LLM integration.

---

