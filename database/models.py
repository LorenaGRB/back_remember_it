from pydantic import BaseModel
from datetime import datetime
from typing import List
from bson import ObjectId

class Sentence():
    sentence: str
    date: datetime = datetime.timestamp(datetime.now())
class Word():
    name: str    
    context: str    
    is_active: bool = True
    creation: datetime = datetime.timestamp(datetime.now())
    sentences: List[Sentence] = []
class User(BaseModel):
    _id: ObjectId
    username: str
    pwd: str
    email: str
    fullname: str
    mobile_tkn: str
    creation_date: datetime = datetime.timestamp(datetime.now())
    words: List[Word] = []
