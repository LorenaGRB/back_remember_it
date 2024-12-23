from pymongo.collection import Collection
from bson import ObjectId
from app.db import db
from app.schemas.user_schema import UserSchema

class UserRepository:
    def __init__(self, collection: Collection = db.users):
        self.collection = collection

    async def get_all_users(self):
        cursor = self.collection.find().limit(100)
        users = []
        async for user in cursor:
            user_dict = dict(user)
            user_dict["id"] = str(user_dict.pop("_id"))
            users.append(user_dict)
        return users

    async def add_user(self, user_data: UserSchema):
        user_data["_id"] = ObjectId() 
        result = await self.collection.insert_one(user_data)
        if not result.inserted_id:
            return None
        user_dict = dict(user_data)
        user_dict["id"] = str(user_dict.pop("_id"))
        return user_dict

    async def get_user_by_id(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        user_dict = dict(user)
        user_dict["id"] = str(user_dict.pop("_id"))
        return user_dict

    async def get_user_by_username(self, username: str):
        user = await self.collection.find_one({"username": username})
        if not user:
            return None
        user_dict = dict(user)
        user_dict["id"] = str(user_dict.pop("_id"))
        return user_dict