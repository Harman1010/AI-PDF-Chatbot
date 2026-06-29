from source.rerank import rerank
from source.guardrails import validate_input

from source.gateway import stream

threshold = 1.82
min_K = 2
max_K = 10

def ask_pdf(query,history,vectorstore):

    allowed,message = validate_input(query)

    if not allowed:
        yield message
        return

    results = vectorstore.similarity_search_with_score(
        query,k=max_K
    )

    if not results:
        yield "I couldn't find relevant information in the uploaded document."
        return

    top_docs = []

    for doc,score in results:
        if score < threshold:
            top_docs.append(doc)
    
    if len(top_docs) < min_K:
        top_docs = [
            doc for doc,score in results[:min_K]
        ]

    top_docs = rerank(query,top_docs)

    context = "\n\n".join(
        [doc.page_content for doc in top_docs]
    )

    sources = set()

    for doc in top_docs:

        if "page" in doc.metadata:

            sources.add(
                f"Page {doc.metadata['page'] + 1}"
            )
    chat_history = ""

    for message in history[-3:]:

        chat_history += (
            f"User: {message['question']}\n"
            f"Assistant: {message['answer']}\n\n"
        )
        
    prompt = f"""
You are a helpful PDF assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
clearly mention that the document does not contain the answer.

Previous Conversation:
{chat_history}

Context:
{context}

Question:
{query}

Answer:
"""

    try:

        response = stream(prompt)

        answer = ""

        for chunk in response:

            answer += chunk

            yield chunk

        if "document does not contain" not in answer.lower():

            yield (
                f"\n\nSources: "
                f"{', '.join(sorted(sources))}"
            )

    except Exception as e:

        yield f"\n\n API Error: {str(e)}"