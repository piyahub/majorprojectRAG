from app.db.mongodb import documents_collection
from app.db.chroma import vectorstore
from app.services.llm_service import generate_answer


def ingest_documents_to_chroma():
    """
    Load documents from MongoDB into ChromaDB (run once).
    """
    docs = documents_collection.find()

    texts = []
    metadatas = []

    for doc in docs:
        texts.append(doc.get("text", ""))
        metadatas.append({
            "category": doc.get("category"),
            "source": doc.get("source"),
            "department": doc.get("department")
        })

    if texts:
        vectorstore.add_texts(texts=texts, metadatas=metadatas)
        vectorstore.persist()


def rag_chat(query: str) -> str:
    """
    Vector-based RAG using ChromaDB
    """
    # 1. Retrieve top 3 relevant documents
    docs = vectorstore.similarity_search(query, k=3)

    if not docs:
        return "Information not available in the documents."

    # 2. Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])

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

    return generate_answer(prompt)
