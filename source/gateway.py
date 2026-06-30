from source.providers.gemini import stream as gemini_stream
from source.providers.groq import stream as groq_stream
from source.providers.mistral import stream as mistral_stream

from datetime import datetime,timedelta

providers = {
    "gemini" : None,
    "groq" : None,
    "mistral" : None
}

def provider_available(provider):
    cooldown = providers[provider]
    if cooldown is None:
        return True
    return datetime.now() >= cooldown

def failure(provider,seconds=60):
    providers[provider] = datetime.now() + timedelta(seconds=seconds)

def stream(prompt):

    if provider_available("gemini"):
        try:

            print("Using Gemini...")

            for chunk in gemini_stream(prompt):

                if chunk.content:

                    yield chunk.content

            return

        except Exception as e:

            message = str(e).lower()

            if "daily" in message:
                failure("gemini", seconds=86400)

            elif "resource_exhausted" in message or "429" in message:
                failure("gemini", seconds=60)

            else:
                failure("gemini", seconds=30)

            print(f"Gemini failed: {e}")

    else:
        print("Cooldown Active")
    if provider_available("groq"):
        try:

            print("Switching to Groq...")

            for chunk in groq_stream(prompt):

                text = chunk.choices[0].delta.content

                if text:

                    yield text

            return

        except Exception as e:

            message = str(e).lower()

            if "daily" in message:
                failure("groq", seconds=86400)

            elif "resource_exhausted" in message or "429" in message:
                failure("groq", seconds=60)

            else:
                failure("groq", seconds=30)

            print(f"Groq failed: {e}")

    if provider_available("mistral"):
        try:

            print("Switching to Mistral...")

            for event in mistral_stream(prompt):

                text = event.choices[0].delta.content

                if text:

                    yield text

            return

        except Exception as e:

            message = str(e).lower()

            if "daily" in message:
                failure("mistral", seconds=86400)

            elif "resource_exhausted" in message or "429" in message:
                failure("mistral", seconds=60)

            else:
                failure("mistral", seconds=30)

            print(f"Mistral failed: {e}")

            raise Exception(
                "All LLM providers failed."
            )
        