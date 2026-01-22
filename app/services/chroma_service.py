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

 
