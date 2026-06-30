from mistralai.client import Mistral

from source.config import MISTRAL_API_KEY

client = Mistral(api_key=MISTRAL_API_KEY)

def stream(prompt):
    response = client.chat.stream(
        model = "mistral-small-2506",
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        
    )
    return response