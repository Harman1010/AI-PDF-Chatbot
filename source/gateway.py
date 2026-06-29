from source.providers.gemini import stream as gemini_stream
from source.providers.groq import stream as groq_stream
from source.providers.mistral import stream as mistral_stream


def stream(prompt):

    try:

        print("Using Gemini...")

        for chunk in gemini_stream(prompt):

            if chunk.content:

                yield chunk.content

        return

    except Exception as e:

        print(f"Gemini failed: {e}")

    try:

        print("Switching to Groq...")

        for chunk in groq_stream(prompt):

            text = chunk.choices[0].delta.content

            if text:

                yield text

        return

    except Exception as e:

        print(f"Groq failed: {e}")

    try:

        print("Switching to Mistral...")

        for event in mistral_stream(prompt):

            text = event.choices[0].delta.content

            if text:

                yield text

        return

    except Exception as e:

        print(f"Mistral failed: {e}")

        raise Exception(
            "All LLM providers failed."
        )