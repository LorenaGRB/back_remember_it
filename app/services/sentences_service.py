from app.repositories.word_repository import WordRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import get_user_by_id
from app.utils.exceptions import NOT_FOUND, INTERNAL_ERROR
from datetime import datetime

user_repo = UserRepository()
word_repo = WordRepository()

async def get_all_sentences(user_id:str,word_data:dict):
    user = await get_user_by_id(user_id)

    words = user["words"]
    matching_word = next((w for w in words if w["name"] == word_data["name"] and w["context"] == word_data["context"]), None)
    return matching_word["sentences"] if matching_word else []


async def create_sentence_service(user_id: str, words_data: list):
  try:
    user = await user_repo.get_user_by_id(user_id)
    if not user:
      raise NOT_FOUND(detail="User not found")
    current_words = user["words"]
    for word in words_data:
      name = word["name"]
      context = word["context"]
      sentence = word["sentence"]
      current_word = next((w for w in current_words if w["name"] == name and w["context"] == context), None)
      print(current_word)
      if current_word:
        current_word["sentences"].append(sentence)
        await word_repo.update_sentences(user_id, name, context, current_word["sentences"])

  except Exception as e:
      print("Error in create sentence service:", e)
      raise INTERNAL_ERROR()