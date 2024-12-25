from app.repositories.word_repository import WordRepository
from app.repositories.user_repository import UserRepository
from app.schemas.word_schema import AddWordInput
from app.services.user_service import get_user_by_id
from app.utils.exceptions import NOT_FOUND
from app.validators.word_validator import validate_word_not_exists, validate_word_schema

user_repo = UserRepository()
word_repo = WordRepository()

async def get_all_sentences(user_id:str,word:str,context:str):
    user = await get_user_by_id(user_id)
    words = user["words"]
    matching_word = next((w for w in words if w["name"] == word and w["context"] == context), None)
    return matching_word["sentences"] if matching_word else []


    