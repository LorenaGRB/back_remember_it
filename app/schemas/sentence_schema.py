from datetime import datetime
from typing import Dict
from pydantic import BaseModel, Field

class SentenceSchema(BaseModel):
    sentence: str
    date: datetime

class GenerateSentenceSchemaInput(BaseModel):
    name: str
    context: str