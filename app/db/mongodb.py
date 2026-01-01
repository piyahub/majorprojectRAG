from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client["rag_chatbot"]

documents_collection = db["documents"]
