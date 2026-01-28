
# import re
# from pathlib import Path

# from app.core.config import settings
# from app.db.chroma import vectorstore
# from langchain_google_genai import ChatGoogleGenerativeAI


# # 🔹 Gemini LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=settings.GEMINI_API_KEY,
#     temperature=0.3,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# # =====================================================
# # 🔹 PROFANITY CHECK SETUP
# # =====================================================

# PROFANITY_SET: set[str] = set()


# def load_profanity_list():
#     """
#     Loads profanity words from file into memory (once).
#     """
#     global PROFANITY_SET

#     profanity_file = Path(settings.DATA_DIR) / "profanity_list.txt"

#     if not profanity_file.exists():
#         print("⚠️ Profanity list not found. Profanity check disabled.")
#         return

#     with open(profanity_file, "r", encoding="utf-8") as f:
#         PROFANITY_SET = {
#             line.strip().lower()
#             for line in f
#             if line.strip()
#         }

#     print(f"✅ Loaded {len(PROFANITY_SET)} profanity words.")


# def contains_profanity(text: str) -> bool:
#     """
#     Checks if input text contains profanity.
#     """
#     if not PROFANITY_SET:
#         return False

#     words = set(re.split(r"\W+", text.lower()))
#     return not PROFANITY_SET.isdisjoint(words)


# # 🔹 Load profanity list at startup
# load_profanity_list()

# # =====================================================
# # 🔹 RAG CHAT FUNCTION
# # =====================================================

# def rag_chat(query: str) -> str:
#     """
#     Perform Retrieval-Augmented Generation (RAG)
#     using ChromaDB + Gemini
#     """

#     # 🚨 STEP 0: PROFANITY CHECK (BEFORE RAG)
#     if contains_profanity(query):
#         return "❌ Inappropriate language detected. Please rephrase your question."

#     # 1️⃣ Retrieve relevant documents
#     docs = vectorstore.similarity_search(query, k=3)

#     if not docs:
#         return "Information not available in the documents."

#     # 2️⃣ Build context
#     context = "\n\n".join(doc.page_content for doc in docs)

#     prompt = f"""
# You are a helpful college assistant.
# Answer ONLY using the context below.
# If the answer is not found, say "Information not available in the documents."

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     # 3️⃣ Gemini call
#     response = llm.invoke(prompt)
#     return response.content







import re
import uuid
from pathlib import Path
from typing import Dict, List

from app.core.config import settings
from app.db.chroma import vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI

# =====================================================
# 🔹 IN-MEMORY CHAT STORAGE
# =====================================================

# {
#   session_id: [
#       {"role": "user", "content": "..."},
#       {"role": "assistant", "content": "..."}
#   ]
# }
CHAT_SESSIONS: Dict[str, List[dict]] = {}

# =====================================================
# 🔹 GEMINI LLM
# =====================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# =====================================================
# 🔹 PROFANITY CHECK
# =====================================================

PROFANITY_SET: set[str] = set()


def load_profanity_list():
    profanity_file = Path(settings.DATA_DIR) / "profanity_list.txt"

    if not profanity_file.exists():
        print("⚠️ Profanity list not found. Profanity check disabled.")
        return

    with open(profanity_file, "r", encoding="utf-8") as f:
        PROFANITY_SET.update(
            line.strip().lower()
            for line in f
            if line.strip()
        )

    print(f"✅ Loaded {len(PROFANITY_SET)} profanity words.")


def contains_profanity(text: str) -> bool:
    if not PROFANITY_SET:
        return False
    words = set(re.split(r"\W+", text.lower()))
    return not PROFANITY_SET.isdisjoint(words)


load_profanity_list()

# =====================================================
# 🔹 RAG CHAT (WITH MEMORY)
# =====================================================

# def rag_chat(query: str, session_id: str | None = None) -> dict:
#     """
#     RAG + Gemini + In-memory chat session
#     """

#     # 🔹 Create / reuse session
#     if session_id is None:
#         session_id = str(uuid.uuid4())

#     if session_id not in CHAT_SESSIONS:
#         CHAT_SESSIONS[session_id] = []

#     chat_history = CHAT_SESSIONS[session_id]

#     # 🚨 PROFANITY CHECK
#     if contains_profanity(query):
#         return {
#             "session_id": session_id,
#             "answer": "❌ Inappropriate language detected. Please rephrase your question."
#         }

#     # 🔹 Save user message
#     chat_history.append({"role": "user", "content": query})

#     # 1️⃣ Retrieve documents
#     docs = vectorstore.similarity_search(query, k=3)

#     if not docs:
#         return {
#             "session_id": session_id,
#             "answer": "Information not available in the documents."
#         }

#     # 2️⃣ Build context
#     context = "\n\n".join(doc.page_content for doc in docs)

#     # 🔹 Build conversation memory (last 5 messages)
#     conversation = ""
#     for msg in chat_history[-5:]:
#         role = "User" if msg["role"] == "user" else "Assistant"
#         conversation += f"{role}: {msg['content']}\n"

#     prompt = f"""
# You are a helpful college assistant.
# Use the conversation history to answer follow-up questions.

# Conversation:
# {conversation}

# Use ONLY the context below.
# If the answer is not found, say "Information not available in the documents."

# Context:
# {context}

# Current Question:
# {query}

# Answer:
# """

#     # 3️⃣ Gemini call
#     response = llm.invoke(prompt)

#     # 🔹 Save assistant response
#     chat_history.append({"role": "assistant", "content": response.content})

#     return {
#         "session_id": session_id,
#         "answer": response.content
#     }
def rag_chat(query: str, session_id: str | None = None) -> dict:
    """
    RAG + Gemini + In-memory chat session (history-aware retrieval)
    """

    # 🔹 Create / reuse session
    if session_id is None:
        session_id = str(uuid.uuid4())

    if session_id not in CHAT_SESSIONS:
        CHAT_SESSIONS[session_id] = []

    chat_history = CHAT_SESSIONS[session_id]

    # 🚨 PROFANITY CHECK
    if contains_profanity(query):
        return {
            "session_id": session_id,
            "answer": "❌ Inappropriate language detected. Please rephrase your question."
        }

    # 🔹 Save user message
    chat_history.append({"role": "user", "content": query})

    # =====================================================
    # 🔹 HISTORY-AWARE RETRIEVAL (🔥 KEY FIX 🔥)
    # =====================================================

    # Use last 3 user+assistant turns for retrieval context
    history_text = ""
    for msg in chat_history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    retrieval_query = f"""
Conversation so far:
{history_text}

Current question:
{query}
"""

    # 1️⃣ Retrieve documents USING rewritten query
    docs = vectorstore.similarity_search(retrieval_query, k=3)

    if not docs:
        return {
            "session_id": session_id,
            "answer": "Information not available in the documents."
        }

    # 2️⃣ Build context
    context = "\n\n".join(doc.page_content for doc in docs)

    # =====================================================
    # 🔹 FINAL PROMPT TO LLM
    # =====================================================

    prompt = f"""
You are a helpful college assistant.
Use the conversation history to answer follow-up questions.

Conversation:
{history_text}

Use ONLY the context below.
If the answer is not found, say "Information not available in the documents."

Context:
{context}

Current Question:
{query}

Answer:
"""

    # 3️⃣ Gemini call
    response = llm.invoke(prompt)

    # 🔹 Save assistant response
    chat_history.append({"role": "assistant", "content": response.content})

    return {
        "session_id": session_id,
        "answer": response.content
    }

