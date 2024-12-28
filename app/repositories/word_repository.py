from datetime import datetime
from http.client import NOT_FOUND
from bson import ObjectId
from pymongo.collection import Collection
from app.db import db
from app.schemas.user_schema import UserSchema
from app.schemas.word_schema import WordSchema
from app.services.user_service import get_user_by_id
from app.utils.exceptions import INTERNAL_ERROR
from typing import List

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
      
  async def get_all_words(self, user_id: str, page: int = 1, page_size: int = 10) -> List[dict]:
    try:
      user = await get_user_by_id(user_id)
      words = user["words"]
      offset = (page - 1) * page_size
      return words[offset: offset + page_size]
    except:
      raise INTERNAL_ERROR()

  async def update_sentences(self, user_id: str, word_name: str, context: str, new_sentences: list):
    try:
      res = await self.collection.update_one(
        {"_id": ObjectId(user_id), "words.name": word_name, "words.context": context},
        {"$set": {"words.$.sentences": new_sentences}}
      )
      return res
    except:
      raise INTERNAL_ERROR()