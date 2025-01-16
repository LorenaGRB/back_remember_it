from datetime import date
from typing import Dict
from pydantic import BaseModel, Field

class SentenceSchema(BaseModel):
    sentence: str
    notification_planned_date: date
    notification_sent: bool

class GenerateSentenceSchemaInput(BaseModel):
    name: str
    context: str