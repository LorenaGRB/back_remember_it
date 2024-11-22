from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List

class SentenceSchema(BaseModel):
    sentence: str
    date: datetime

class WordSchema(BaseModel):
    name: str
    context: str
    is_active: bool
    creation_date: datetime
    sentences: List[SentenceSchema] = []

class UserSchema(BaseModel):
    username: str
    pwd: str
    email: EmailStr
    fullname: str
    mobile_tkn: str
    words: List[WordSchema] = []

class UserResponse(UserSchema):
    id: str = Field(..., alias="id")
