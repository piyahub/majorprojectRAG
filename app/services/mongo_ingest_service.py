from app.db.mongodb import db
from app.services.chroma_service import add_documents_to_chroma


# ---------- FORMATTERS ----------

def format_classtable(doc):
    day = doc.get("day", "unknown day")
    sem = doc.get("sem", "unknown semester")
    slot = doc.get("slot", "unknown slot")

    texts = []
    for entry in doc.get("slotData", []):
        subject = entry.get("subject") or "subject not assigned"
        faculty = entry.get("faculty") or "faculty not assigned"
        room = entry.get("room") or "room not assigned"

        texts.append(
            f"On {day}, for {sem}, during {slot}, "
            f"the subject is {subject}, taught by {faculty}, in room {room}."
        )

    return " ".join(texts)


def format_addrooms(doc):
    room = doc.get("room", "unknown room")
    room_type = doc.get("type", "unknown type")
    return f"{room} is a {room_type}."


def format_addsems(doc):
    sem = doc.get("sem", "unknown semester")
    return f"The semester is {sem}."


def format_subjects(doc):
    return (
        f"{doc.get('subjectFullName')} ({doc.get('subCode')}) "
        f"is a {doc.get('type')} subject for {doc.get('sem')} "
        f"in the {doc.get('dept')} department."
    )


def format_notes(doc):
    faculty = doc.get("faculty", "unknown faculty")
    sem = doc.get("sem", "unknown semester")
    room = doc.get("room", "unknown room")
    note_text = " ".join(doc.get("note", []))

    return (
        f"Notes for {sem} were uploaded by {faculty} "
        f"for {room}. Content: {note_text}"
    )


# def format_addfaculties(doc):
#     names = ", ".join(doc.get("faculty", []))
#     sem = doc.get("sem", "unknown semester")
#     return f"The faculty members for {sem} are {names}."

def format_addfaculties(doc):
    faculty_list = doc.get("faculty", [])

    cleaned_names = []

    for item in faculty_list:
        if isinstance(item, str):
            cleaned_names.append(item)
        elif isinstance(item, list):
            cleaned_names.extend(
                [name for name in item if isinstance(name, str)]
            )

    if not cleaned_names:
        names = "no faculty assigned"
    else:
        names = ", ".join(cleaned_names)

    sem = doc.get("sem", "unknown semester")

    return f"Faculties {names} are assigned to semester {sem}."



def format_faculties(doc):
    return (
        f"{doc.get('name')} is an {doc.get('designation')} "
        f"in the {doc.get('dept')} department. "
        f"Email: {doc.get('email')}."
    )


def format_allotments(doc):
    return (
        f"{doc.get('subject')} is allotted to "
        f"{doc.get('faculty')} for {doc.get('semester')}."
    )


# ---------- COLLECTION MAP ----------

COLLECTION_FORMATTERS = {
    "classtables": format_classtable,
    "addrooms": format_addrooms,
    "addsems": format_addsems,
    "subjects": format_subjects,
    "notes": format_notes,
    "addfaculties": format_addfaculties,
    "faculties": format_faculties,
    "allotments": format_allotments,
}


# ---------- INGEST ----------

# def ingest_selected_collections():
#     for collection_name, formatter in COLLECTION_FORMATTERS.items():
#         collection = db[collection_name]
#         texts = []

#         for doc in collection.find():
#             text = formatter(doc)
#             if text.strip():
#                 texts.append(text)

#         if texts:
#             add_documents_to_chroma(
#                 texts=texts,
#                 metadata={"collection": collection_name}
#             )


# def ingest_selected_collections():
#     for collection_name, formatter in COLLECTION_FORMATTERS.items():
#         collection = db[collection_name]

#         texts = []

#         # FIX-2 + FIX-3 applied here
#         cursor = collection.find(
#             {},
#             {"_id": 0}
#         ).batch_size(200)

#         for doc in cursor:
#             text = formatter(doc)
#             if text.strip():
#                 texts.append(text)

#         if texts:
#             add_documents_to_chroma(
#                 texts=texts,
#                 metadata={"collection": collection_name}
#             )

def ingest_selected_collections():
    BATCH_SIZE = 50   # 🔥 critical

    for collection_name, formatter in COLLECTION_FORMATTERS.items():
        print(f"[INGEST] Processing collection: {collection_name}")

        collection = db[collection_name]
        texts_batch = []
        total_docs = 0

        cursor = collection.find({}, {"_id": 0}).batch_size(200)

        for doc in cursor:
            text = formatter(doc)
            if text.strip():
                texts_batch.append(text)

            if len(texts_batch) >= BATCH_SIZE:
                add_documents_to_chroma(
                    texts=texts_batch,
                    metadata={"collection": collection_name}
                )
                total_docs += len(texts_batch)
                print(f"[INGEST] {collection_name}: {total_docs} added")

                texts_batch.clear()  # 🔥 free memory

        # Insert remaining docs
        if texts_batch:
            add_documents_to_chroma(
                texts=texts_batch,
                metadata={"collection": collection_name}
            )
            total_docs += len(texts_batch)

        print(f"[INGEST] {collection_name}: DONE ({total_docs} docs)")


