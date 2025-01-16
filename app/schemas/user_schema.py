from pydantic import BaseModel, Field, EmailStr
from typing import List
from app.schemas.word_schema import WordSchema
class UserSchema(BaseModel):
    username: str
    pwd: str
    email: EmailStr
    fullname: str
    mobile_tkn: str
    words: List[WordSchema] = []
class UserResponse(UserSchema):
    id: str = Field(..., alias="id")

class UserToLogin(BaseModel):
    username: str
    pwd: str

class LoginResponse(BaseModel):
    access_token: str

class SaveUserTokenInput(BaseModel):
    user_id: str
    mobile_token: str