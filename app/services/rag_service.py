
from app.db.chroma import vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


# 🔹 Gemini LLM (moved here from llm_service.py)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def rag_chat(query: str) -> str:
    """
    Perform Retrieval-Augmented Generation (RAG)
    using ChromaDB + Gemini
    """

    # 1️⃣ Retrieve relevant documents
    docs = vectorstore.similarity_search(query, k=3)

    if not docs:
        return "Information not available in the documents."

    # 2️⃣ Build context
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful college assistant.
Answer ONLY using the context below.
If the answer is not found, say "Information not available in the documents."

Context:
{context}

Question:
{query}

Answer:
"""

    # 3️⃣ Gemini call
    response = llm.invoke(prompt)
    return response.content
