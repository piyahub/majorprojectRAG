import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "RAG Chatbot"
    MONGO_URI = os.getenv("MONGO_URI")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") 
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
    DATA_DIR = os.getenv("DATA_DIR", "app/data")

settings = Settings()
