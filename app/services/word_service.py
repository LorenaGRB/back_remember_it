from app.repositories.word_repository import WordRepository
from app.repositories.user_repository import UserRepository
from app.schemas.word_schema import AddWordInput
from app.utils.exceptions import NOT_FOUND
from app.validators.word_validator import validate_word_not_exists, validate_word_schema

user_repo = UserRepository()
word_repo = WordRepository()

async def add_word(input_data: AddWordInput):
    data = dict(input_data)
    user_id = str(data["id"])
    word_to_add = dict(data["word"])
    user = await user_repo.get_user_by_id(user_id)
    if(user):
        validate_word_schema(word_to_add)
        await validate_word_not_exists(word_to_add, dict(user))

        updated_user = await word_repo.add_word_to_user(word_to_add,user_id)
        return updated_user
    else:
        raise NOT_FOUND("User id is not valid")