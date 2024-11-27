from app.schemas.word_schema import WordSchema
from app.utils.exceptions import INTERNAL_ERROR, NOT_FOUND

def validate_word_schema(word_to_add: WordSchema):
    if not word_to_add["name"]:
        raise NOT_FOUND(detail="Word is required")
    if not word_to_add["context"]:
        raise NOT_FOUND(detail="Context is required")

async def validate_word_not_exists(word_data: dict,user: dict) -> dict:
    name = word_data["name"]
    context= word_data["context"]
    for word in user["words"]:
        if((word["name"] == name) or (word["context"] == context)):
            raise INTERNAL_ERROR(detail="The word already exists")