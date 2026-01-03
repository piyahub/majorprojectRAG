
from app.db.mongodb import documents_collection
from app.db.chroma import vectorstore
from langchain_core.documents import Document


def ingest_documents():
    docs = []
    for record in documents_collection.find():
        content = record.get("content") or record.get("text")
        if not content:
            continue

        docs.append(
            Document(
                page_content=content,
                metadata={"source": "mongodb"}
            )
        )

    if docs:
        vectorstore.add_documents(docs)
        # vectorstore.persist()
        print(f"✅ Ingested {len(docs)} documents into Chroma")
    else:
        print("❌ No documents found")

if __name__ == "__main__":
    ingest_documents()
