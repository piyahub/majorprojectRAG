from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_chat

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = rag_chat(request.query)
    return {"answer": answer}
