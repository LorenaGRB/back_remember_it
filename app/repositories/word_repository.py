

from datetime import datetime
from http.client import NOT_FOUND
from bson import ObjectId
from pymongo.collection import Collection
from app.db import db
from app.schemas.user_schema import UserSchema
from app.schemas.word_schema import WordSchema
from app.services.user_service import get_user_by_id
from app.utils.exceptions import INTERNAL_ERROR

class WordRepository:
    def __init__(self, collection: Collection = db.users):
        self.collection = collection
        
    async def add_word_to_user(self, word_data: dict,user_id: str, ) -> dict:
        try:
            self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"words": word_data}}
            )
            return word_data
        except:
            raise INTERNAL_ERROR()
        
    async def get_all_words(self, id: str) -> dict:
        try:
            user = await get_user_by_id(id)
            words = user["words"]
            return words
        except:
            raise INTERNAL_ERROR()
