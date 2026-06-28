from langsmith import Client
from google import genai

from source.chatbot import ask_pdf
from backend import state

client = Client()

gen_ai_client = genai.Client()

dataset_name = "AI Document Assistant Evaluation"


def rag_app(question):

    answer = ""

    for chunk in ask_pdf(

        query=question,
        history=[],
        vectorstore=state.vectorstore

    ):

        answer += chunk

    if "Sources:" in answer:

        answer = answer.split("Sources:")[0].strip()

    return answer


def ls_target(inputs):

    return {

        "response":
        rag_app(inputs["question"])

    }


EVAL_INSTRUCTIONS = """
You are an expert evaluator.

Evaluate ONLY using the reference answer.

Return only the requested output.
"""


def correctness(inputs, outputs, reference_outputs):

    prompt = f"""
Question:
{inputs["question"]}

Reference Answer:
{reference_outputs["answer"]}

Generated Answer:
{outputs["response"]}

Respond ONLY:

CORRECT

or

INCORRECT
"""

    result = gen_ai_client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt,

        config={

            "system_instruction": EVAL_INSTRUCTIONS,

            "temperature":0

        }

    ).text.strip()

    return result.upper() == "CORRECT"


def relevance(inputs, outputs):

    prompt = f"""
Question:
{inputs["question"]}

Generated Answer:
{outputs["response"]}

Does the generated answer directly answer
the user's question?

Respond ONLY:

RELEVANT

or

IRRELEVANT
"""

    result = gen_ai_client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt,

        config={

            "temperature":0

        }

    ).text.strip()

    return result.upper() == "RELEVANT"


def concision(outputs, reference_outputs):

    return len(outputs["response"]) <= (

        2 * len(reference_outputs["answer"])

    )


experiment = client.evaluate(

    ls_target,

    data=dataset_name,

    evaluators=[

        correctness,

        relevance,

        concision

    ],

    experiment_prefix="rag-evaluation"

)

print(experiment.to_pandas())