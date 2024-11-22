from pymongo.collection import Collection
from bson import ObjectId
from app.db import db
from app.schemas.user_schema import UserSchema

class UserRepository:
    def __init__(self, collection: Collection = db.users):
        self.collection = collection

    async def get_all_users(self):
        users = self.collection.find()
        return [
            {**user, "id": str(user["_id"])} 
            for user in users.limit(100)
        ]

    async def get_user_by_id(self, user_id: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        user.id = str(user._id)
        return user

    async def add_user(self, user_data: UserSchema):
        user_data["_id"] = ObjectId() 
        result = self.collection.insert_one(user_data)
        if not result.inserted_id:
            return None
        return {**user_data, "id": str(user_data["_id"])}

    async def delete_user(self, user_id: str):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def update_user(self, user_id: str, update_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
