import json
from fastapi import APIRouter
from app.openAPi.openAi_service import generate_service
from app.schemas.sentence_schema import GenerateSentenceSchemaInput
from app.services.sentences_service import get_all_sentences
from app.utils.exceptions import INTERNAL_ERROR
from app.utils.responses import CREATED_RESPONSE, SUCCESS_RESPONSE

router = APIRouter()

@router.post("/generate")
async def generate_sentence(word:GenerateSentenceSchemaInput):
    sentence_generated = await generate_service(word)
    if(sentence_generated):
        return CREATED_RESPONSE(data=sentence_generated)
    else:
        raise INTERNAL_ERROR()

@router.get("/")
async def get_sentences(user_id:str,word:str,context:str):
    sentences = await get_all_sentences(user_id,word,context)
    if(sentences):
        return SUCCESS_RESPONSE(data=sentences)
    else:
        raise INTERNAL_ERROR()