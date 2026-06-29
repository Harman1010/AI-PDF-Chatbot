from langchain_google_genai import ChatGoogleGenerativeAI

from source.config import API_KEY


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=API_KEY
)


def stream(prompt):

    return model.stream(prompt)