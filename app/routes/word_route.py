import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.schemas.word_schema import AddWordInput
from app.services.word_service import add_word, get_all_words
from app.utils.exceptions import INTERNAL_ERROR
from app.utils.responses import CREATED_RESPONSE, SUCCESS_RESPONSE
from app.middlewares.auth import AuthenticationMiddleware

router = APIRouter()
auth  = AuthenticationMiddleware()

@router.post("/", dependencies = [Depends(auth)])
async def create_word(word_data:AddWordInput):
    updated_user = await add_word(word_data)
    if(updated_user):
        return CREATED_RESPONSE(data=updated_user)
    else:
        raise INTERNAL_ERROR()
    
@router.get("/", dependencies = [Depends(auth)])
async def get_words(user_id:str):
    words = await get_all_words(user_id)
    if(words):
        return SUCCESS_RESPONSE(data=words)
    else:
        raise INTERNAL_ERROR()