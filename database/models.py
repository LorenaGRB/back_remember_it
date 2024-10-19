from pydantic import BaseModel
from datetime import datetime
from typing import List

class Sentence(BaseModel):
    sentence: str
    date: str

class Word(BaseModel):
    name: str    
    context: str    
    sentences: List[Sentence] = []
    is_completed: bool = False
    creation: int = int(datetime.timestamp(datetime.now()))

