from app.repositories.word_repository import WordRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import get_user_by_id
from app.utils.exceptions import NOT_FOUND, INTERNAL_ERROR
from datetime import datetime, timedelta

from app.utils.notification_rule import SpaceRules

user_repo = UserRepository()
word_repo = WordRepository()

async def get_all_sentences(user_id:str,word_data:dict):
    user = await get_user_by_id(user_id)

    words = user["words"]
    matching_word = next((w for w in words if w["name"] == word_data["name"] and w["context"] == word_data["context"]), None)
    return matching_word["sentences"] if matching_word else []

def assign_next_notification_date(word_data:dict):
    sentences_amount = len(word_data["sentences"])
    if sentences_amount == SpaceRules.ONE["amount"]:
      current_date = datetime.now()
      return (current_date + timedelta(days=SpaceRules.ONE["days"])).replace(hour=0, minute=0, second=0, microsecond=0)
    before_notification_date = word_data["sentences"][-1]["notification_planned_date"]
    if sentences_amount == SpaceRules.TWO["amount"]:
      return before_notification_date + timedelta(days=SpaceRules.TWO["days"])
    if sentences_amount == SpaceRules.THREE["amount"]:
      return before_notification_date + timedelta(days=SpaceRules.THREE["days"])
    if sentences_amount == SpaceRules.FOUR["amount"]:
      return before_notification_date + timedelta(days=SpaceRules.FOUR["days"])
    if sentences_amount >= SpaceRules.MORE["amount"]:
      return before_notification_date + timedelta(days=SpaceRules.MORE["days"])

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
      next_notification_date = assign_next_notification_date(current_word)
      # print("next_notification_date", next_notification_date)
      new_sentence = {
        "sentence": sentence,
        "notification_planned_date": next_notification_date,
        "notification_sent": False
      }
      if current_word:
        current_word["sentences"].append(new_sentence)
        print("current_word", current_word)
        await word_repo.update_sentences(user_id, name, context, current_word["sentences"])

  except Exception as e:
      print("Error in create sentence service:", e)
      raise INTERNAL_ERROR()