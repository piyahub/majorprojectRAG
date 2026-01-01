import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "RAG Chatbot"
    MONGO_URI = os.getenv("MONGO_URI")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
