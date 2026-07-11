from pydantic import BaseModel
from typing import List, Dict


class ChatRequest(BaseModel):

    session_id : str

    query: str

    history: List[Dict] = []