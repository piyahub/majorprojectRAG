
from app.db.mongodb import documents_collection
from app.db.chroma import vectorstore


def ingest_documents_to_chroma():
    """
    Load documents from MongoDB into ChromaDB.
    Should be run once (or on startup).
    """

    docs = documents_collection.find()

    texts = []
    metadatas = []

    for doc in docs:
        text = doc.get("text", "")
        if not text:
            continue

        texts.append(text)
        metadatas.append({
            "category": doc.get("category"),
            "source": doc.get("source"),
            "department": doc.get("department")
        })

    if texts:
        vectorstore.add_texts(texts=texts, metadatas=metadatas)
        # Chroma auto-persists in new versions
        print(f"✅ Ingested {len(texts)} documents into ChromaDB")
    else:
        print("❌ No documents found in MongoDB")
