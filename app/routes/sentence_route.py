
import json
from fastapi import APIRouter
from app.openAPi.openAi_service import generate_service
from app.schemas.sentence_schema import GenerateSentenceSchemaInput
from app.utils.exceptions import INTERNAL_ERROR
from app.utils.responses import CREATED_RESPONSE

router = APIRouter()

@router.post("/generate")
async def generate_sentence(word:GenerateSentenceSchemaInput):
    sentence_generated = await generate_service(word)
    if(sentence_generated):
        return CREATED_RESPONSE(data= json.dumps(sentence_generated,default=str))
    else:
        raise INTERNAL_ERROR()
    
