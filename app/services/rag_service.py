
import re
from pathlib import Path

from app.core.config import settings
from app.db.chroma import vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI


# 🔹 Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# =====================================================
# 🔹 PROFANITY CHECK SETUP
# =====================================================

PROFANITY_SET: set[str] = set()


def load_profanity_list():
    """
    Loads profanity words from file into memory (once).
    """
    global PROFANITY_SET

    profanity_file = Path(settings.DATA_DIR) / "profanity_list.txt"

    if not profanity_file.exists():
        print("⚠️ Profanity list not found. Profanity check disabled.")
        return

    with open(profanity_file, "r", encoding="utf-8") as f:
        PROFANITY_SET = {
            line.strip().lower()
            for line in f
            if line.strip()
        }

    print(f"✅ Loaded {len(PROFANITY_SET)} profanity words.")


def contains_profanity(text: str) -> bool:
    """
    Checks if input text contains profanity.
    """
    if not PROFANITY_SET:
        return False

    words = set(re.split(r"\W+", text.lower()))
    return not PROFANITY_SET.isdisjoint(words)


# 🔹 Load profanity list at startup
load_profanity_list()

# =====================================================
# 🔹 RAG CHAT FUNCTION
# =====================================================

def rag_chat(query: str) -> str:
    """
    Perform Retrieval-Augmented Generation (RAG)
    using ChromaDB + Gemini
    """

    # 🚨 STEP 0: PROFANITY CHECK (BEFORE RAG)
    if contains_profanity(query):
        return "❌ Inappropriate language detected. Please rephrase your question."

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
