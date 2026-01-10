# from pymongo import MongoClient
# from app.core.config import settings

# client = MongoClient(settings.MONGO_URI)
# db = client["simple_rag"]

# documents_collection = db["documents"]



from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(
    settings.MONGO_URI,
    connectTimeoutMS=60000,   # 60s
    socketTimeoutMS=60000,    # 60s
    serverSelectionTimeoutMS=60000
)

db = client[settings.MONGO_DB_NAME]
