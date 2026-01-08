from fastapi import FastAPI
from app.api.v1.routes.chat import router as chat_router
from app.services.chroma_service import ingest_documents_to_chroma
from app.core.config import settings
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def startup_event():
    ingest_documents_to_chroma()

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Vector RAG Chatbot Running"}


