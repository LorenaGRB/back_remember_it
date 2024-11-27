

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.schemas.sentence_schema import SentenceSchema

class WordSchema(BaseModel):
    name: str
    context: str
    is_active: bool
    creation_date: datetime
    sentences: List[SentenceSchema] = []

class WordInput(BaseModel):
    name: str
    context: str
    sentences: List[SentenceSchema] = []

class AddWordInput(BaseModel):
    id: str = Field(..., alias="id")
    word: WordInput
