from pymongo.collection import Collection
from bson import ObjectId
from app.db import db
from app.schemas.user_schema import UserSchema
from app.utils.exceptions import INTERNAL_ERROR

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
    
    async def save_user_token_repository(self, token_info):
      user_id = token_info.user_id
      mobile_token = token_info.mobile_token
      try:
        await self.collection.update_one(
          {"_id": ObjectId(user_id)},
          {"$set": {"mobile_tkn": mobile_token}}
        )
        return {"id": user_id, "mobile_tkn": mobile_token}
      except:
        raise INTERNAL_ERROR()
        
    async def get_mobile_token_repository(self, user_id: str):
      try:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return user["mobile_tkn"]
      except:
        raise INTERNAL_ERROR()