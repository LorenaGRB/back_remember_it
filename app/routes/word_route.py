import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.word_schema import AddWordInput
from app.services.word_service import add_word
from app.utils.exceptions import INTERNAL_ERROR
from app.utils.responses import CREATED_RESPONSE

router = APIRouter()

@router.post("/")
async def create_word(word_data:AddWordInput):
    updated_user = await add_word(word_data)
    if(updated_user):
        return CREATED_RESPONSE(data=updated_user)
    else:
        raise INTERNAL_ERROR()
