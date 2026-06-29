import os
import re

from dotenv import load_dotenv

from langsmith import Client

from groq import Groq

from langchain_community.vectorstores import FAISS

from source.embeddings import get_embeddings
from source.chatbot import ask_pdf

load_dotenv()

client = Client()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DATASET_NAME = "AI Document Assistant Evaluation"

if not os.path.exists("faiss_index"):
    raise FileNotFoundError(
        "No FAISS index found. Please upload a PDF first."
    )

embeddings = get_embeddings()

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

EVAL_INSTRUCTIONS = """
You are an expert evaluator.

Evaluate answers objectively.

Only follow the evaluation rubric.

Return only the requested output.
"""


def evaluate_with_groq(prompt):

    response = groq_client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[

            {
                "role":"system",
                "content":EVAL_INSTRUCTIONS
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )

    return response.choices[0].message.content.strip()


def rag_app(question):

    answer = ""

    for chunk in ask_pdf(

        query=question,

        history=[],

        vectorstore=vectorstore

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


def correctness(inputs, outputs, reference_outputs):

    prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Question:
{inputs["question"]}

Reference Answer:
{reference_outputs["answer"]}

Generated Answer:
{outputs["response"]}

Scoring Rubric

5 = Completely correct

4 = Mostly correct with only minor omissions

3 = Partially correct but misses important information

2 = Mostly incorrect

1 = Completely incorrect

Return ONLY a single integer between 1 and 5.
"""

    result = evaluate_with_groq(prompt)

    match = re.search(r"[1-5]", result)

    if match:

        score = int(match.group())

    else:

        score = 1

    return {
        "score": score / 5
    }


def relevance(inputs, outputs):

    prompt = f"""
Question:

{inputs["question"]}

Generated Answer:

{outputs["response"]}

Does the generated answer directly answer
the user's question?

Respond ONLY

RELEVANT

or

IRRELEVANT
"""

    result = evaluate_with_groq(prompt)

    return result.upper() == "RELEVANT"


def concision(outputs, reference_outputs):

    return len(outputs["response"]) <= (2 * len(reference_outputs["answer"]))


experiment = client.evaluate(

    ls_target,

    data=DATASET_NAME,

    evaluators=[

        correctness,

        relevance,

        concision

    ],

    experiment_prefix="rag-evaluation"

)

print(experiment.to_pandas())