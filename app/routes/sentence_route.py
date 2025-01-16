from fastapi import APIRouter, Depends
from app.external_services.openAiApi.openAi_service import generate_service, send_batch_service,get_batch_list_service, get_batch_status_service, get_batch_results_service,save_sentences_from_batch_service
from app.middlewares.auth import AuthenticationMiddleware
from app.schemas.sentence_schema import GenerateSentenceSchemaInput
from app.utils.exceptions import INTERNAL_ERROR
from app.utils.responses import CREATED_RESPONSE, SUCCESS_RESPONSE

router = APIRouter()
auth  = AuthenticationMiddleware()

@router.post("/generate", dependencies = [Depends(auth)])
async def generate_sentence(word:GenerateSentenceSchemaInput):
  sentence_generated = await generate_service(word)
  if(sentence_generated):
    return CREATED_RESPONSE(data=sentence_generated)
  else:
    raise INTERNAL_ERROR()

@router.get("/send_batch", dependencies = [Depends(auth)])
async def send_batch():
  generated_batch = await send_batch_service()
  if(generated_batch):
    return CREATED_RESPONSE(data=generated_batch)
  else:
    raise INTERNAL_ERROR()

@router.get("/batch_list", dependencies = [Depends(auth)])
async def get_batch_list():
  batch_list = await get_batch_list_service() 
  if(batch_list):
    return SUCCESS_RESPONSE(data=batch_list)
  else:
    raise INTERNAL_ERROR()

@router.get("/batch_status/{batch_id}", dependencies = [Depends(auth)])
async def get_batch_status(batch_id: str):
  batch_job = await get_batch_status_service(batch_id)
  if(batch_job):
    return SUCCESS_RESPONSE(data=batch_job)
  else:
    raise INTERNAL_ERROR()

@router.get("/batch_result/{output_file_id}", dependencies = [Depends(auth)])
async def get_batch_result_service(output_file_id: str):
  result = await get_batch_results_service(output_file_id)
  if(result):
    return SUCCESS_RESPONSE(data=result)
  else:
    raise INTERNAL_ERROR()

@router.get("/save_batch_sentences", dependencies = [Depends(auth)])
async def save_batch_sentences():
  try:
    finished = await save_sentences_from_batch_service()
    if(finished):
      return SUCCESS_RESPONSE()
    else:
      raise INTERNAL_ERROR()
  except Exception as e:
    raise INTERNAL_ERROR()