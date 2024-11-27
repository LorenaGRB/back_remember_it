from pymongo.mongo_client import MongoClient
from app.config import settings

client = MongoClient(settings.DB_MONGO_LOCAL_URL)
db = client[settings.DB_NAME]
users_collection = db["users"]