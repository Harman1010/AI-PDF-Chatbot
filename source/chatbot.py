from langchain_google_genai import ChatGoogleGenerativeAI

from source.config import API_KEY


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=API_KEY
)


def ask_pdf(query,history,retriever):

    docs = retriever.invoke(query)

    if not docs:
        yield "I couldn't find relevant information in the uploaded document."
        return

    top_docs = docs[:3]

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

        response = model.stream(prompt)

        answer = ""

        for chunk in response:

            if chunk.content:

                answer += chunk.content

                yield chunk.content

        if "document does not contain" not in answer.lower():

            yield (
                f"\n\nSources: "
                f"{', '.join(sorted(sources))}"
            )

    except Exception as e:

        yield f"\n\n API Error: {str(e)}"