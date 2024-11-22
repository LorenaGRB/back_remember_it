from pymongo.mongo_client import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URL)
db = client[settings.DB_NAME]
users_collection = db["users"]