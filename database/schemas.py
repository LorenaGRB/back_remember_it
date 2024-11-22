from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from models import Word

def sentence_data(sentence):
    return{
        "sentence": sentence["sentence"] ,
        "date": sentence["date"]
    }

def word_data(word):
    return{
        "id": str(word["_id"]),
        "name": word["name"],
        "context": word["context"],
        "sentences": [sentence_data(sentence) for sentence in word["sentences"]] ,
    }

def all_words(words):
    return [word_data(word) for word in words]

class UserBase(BaseModel):
    username: str
    pwd: str
    email: str
    fullname: str
    mobile_tkn: Optional[str]
    creation_date: datetime = datetime.timestamp(datetime.now())
    words: Optional[List[Word]] = []