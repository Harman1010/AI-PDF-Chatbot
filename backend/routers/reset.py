from fastapi import APIRouter

from backend import state

router = APIRouter(
    prefix="/reset",
    tags=["Reset"]
)


@router.post("/")
def reset():

    state.retriever = None
    
    history = []

    return {
        "message": "Conversation reset successfully."
    }