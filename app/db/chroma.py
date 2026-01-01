from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

embedding_function = GoogleGenerativeAIEmbeddings(
    google_api_key=settings.GEMINI_API_KEY,
    model="models/embedding-001"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)
