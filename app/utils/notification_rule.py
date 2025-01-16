from datetime import datetime, timedelta
from enum import Enum


# def notification_has_to_be_send(word_info):
#   the_notification_was_sended = word_info["sentences"][-1]["notification_date"] is not None
#   if the_notification_was_sended:
#     return False
#   today = datetime.now()
#   last_notification_sended_date = word_info["sentences"][-2]["notification_date"]
#   how_many_sentences_was_sended = len(word_info["sentences"]) -1
#   next_notification_date = applaying_space_repetition_rules(last_notification_sended_date,how_many_sentences_was_sended)
#   return today >= next_notification_date


# def applaying_space_repetition_rules (last_notification_sended_date,how_many_sentences_was_sended):
#   if how_many_sentences_was_sended == 1:
#     return last_notification_sended_date + timedelta(days=1)
#   elif how_many_sentences_was_sended == 2:
#     return last_notification_sended_date + timedelta(days=3)
#   elif how_many_sentences_was_sended == 3:
#     return last_notification_sended_date + timedelta(days=7)
#   elif how_many_sentences_was_sended == 4:
#     return last_notification_sended_date + timedelta(days=15)
#   elif how_many_sentences_was_sended == 5:
#     return last_notification_sended_date + timedelta(days=30)
#   elif how_many_sentences_was_sended == 6:
#     return last_notification_sended_date + timedelta(days=60)
#   elif how_many_sentences_was_sended == 7:
#     return last_notification_sended_date + timedelta(days=120)
#   elif how_many_sentences_was_sended == 8:
#     return last_notification_sended_date + timedelta(days=240)
#   elif how_many_sentences_was_sended == 9:
#     return last_notification_sended_date + timedelta(days=480)
#   elif how_many_sentences_was_sended == 10:
#     return last_notification_sended_date + timedelta(days=960)
#   else:
#     return None

class SpaceRules(Enum):
    ONE = {
      "amount": 1,
      "days": 1
      }
    TWO = {
      "amount": 2,
      "days": 3
      }
    THREE = {
      "amount": 3,
      "days": 7
      }
    FOUR = {
      "amount": 4,
      "days": 15
      }
    MORE = {
      "amount": 5,
      "days": 30
      }

