
from pydantic import BaseModel


class push_notification_input(BaseModel):
    token: str
    message: str
    extra: str