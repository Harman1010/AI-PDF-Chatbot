from groq import Groq

from source.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def stream(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        stream=True)
    
    return response

