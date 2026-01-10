
# from app.db.mongodb import documents_collection
# from app.db.chroma import vectorstore


# def ingest_documents_to_chroma():
#     """
#     Load documents from MongoDB into ChromaDB.
#     Should be run once (or on startup).
#     """

#     docs = documents_collection.find()

#     texts = []
#     metadatas = []

#     for doc in docs:
#         text = doc.get("text", "")
#         if not text:
#             continue

#         texts.append(text)
#         metadatas.append({
#             "category": doc.get("category"),
#             "source": doc.get("source"),
#             "department": doc.get("department")
#         })

#     if texts:
#         vectorstore.add_texts(texts=texts, metadatas=metadatas)
#         # Chroma auto-persists in new versions
#         print(f"✅ Ingested {len(texts)} documents into ChromaDB")
#     else:
#         print("❌ No documents found in MongoDB")





from app.db.chroma import vectorstore

MAX_BATCH_SIZE = 500  # safe limit


def add_documents_to_chroma(texts: list[str], metadata: dict):
    """
    Add documents to Chroma in safe batches.
    """
    total = len(texts)

    for i in range(0, total, MAX_BATCH_SIZE):
        batch_texts = texts[i:i + MAX_BATCH_SIZE]
        batch_metadata = [metadata] * len(batch_texts)

        vectorstore.add_texts(
            texts=batch_texts,
            metadatas=batch_metadata
        )

    vectorstore.persist()
