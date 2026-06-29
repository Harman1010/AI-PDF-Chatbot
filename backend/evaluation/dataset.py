from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()

dataset_name = "AI Document Assistant Evaluation"

dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Evaluation dataset for AI Document Assistant"
)

client.create_examples(

    inputs=[

        {
            "question":
            "What are Harman's skills?"
        },

        {
            "question":
            "What backend technologies does Harman know?"
        },

        {
            "question":
            "What projects has Harman built?"
        },

        {
            "question":
            "Explain FastAPI."
        },

        {
            "question":
            "Who is the Prime Minister of Japan?"
        }

    ],

    outputs=[

        {
            "answer":
            "Harman's skills include Python, SQL, C++, JavaScript, PyTorch, Scikit-learn, FastAPI, SQLite, SQLAlchemy, LangChain, LangGraph, Hugging Face and related technologies."
        },

        {
            "answer":
            "Harman has experience with FastAPI, REST APIs, SQLite, SQLAlchemy and API Integration."
        },

        {
            "answer":
            "Harman has built AI Document Assistant, Customer Churn Prediction and Kepler Planet Signal Review System."
        },

        {
            "answer":
            "The uploaded document does not explain FastAPI."
        },

        {
            "answer":
            "The uploaded document does not contain this information."
        }

    ],

    dataset_id=dataset.id

)

print("Dataset Created Successfully!")