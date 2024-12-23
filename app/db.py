from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.DB_MONGO_LOCAL_URL)
db = client[settings.DB_NAME]
users_collection = db["users"]