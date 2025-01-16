from app.schemas.sentence_schema import GenerateSentenceSchemaInput
from app.external_services.openAiApi.openAI_config import openAI
from app.services.user_service import get_all_users
from app.services.sentences_service import create_sentence_service
import json
import os
from openai import OpenAI

from app.utils.exceptions import INTERNAL_ERROR

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI() 

async def generate_service(word: GenerateSentenceSchemaInput):
    prompt = f"Create a not too long sentence in english using the word {word.name},consider sentence context is {word.context}"
    completion = openAI.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1.5,
        max_tokens=50,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    sentence = completion.choices[0].message.content
    return sentence

async def send_batch_service():
  data = await get_all_users()
  requests = []
  for user in data:
    user_id = user["id"]
    words = user["words"]
    for  word in words:
      name = word.get("name")
      context = word.get("context")
      word_obj = {
        "custom_id": f"{user_id}-{name}-{context}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
          "model": "gpt-4o-mini",
          "temperature": 1.0,
          "messages": [
            {
              "role": "system",
              "content": "You are a helpful assistant."
            },
            {
              "role": "user",
              "content": f"Create a not too long sentence in english using the word {name},consider sentence context is {context}"
            }
          ],
        }
      }
      requests.append(word_obj)
  #creating the file jsonl
  file_name = "data/batch_requests.jsonl"

  with open(file_name, 'w') as file:
    for obj in requests:
      file.write(json.dumps(obj) + '\n')
  
  batch_file = client.files.create(
    file=open(file_name, "rb"),
    purpose="batch"
  )
  batch_job = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
  )
  batch_job_json = batch_job.to_dict()
  print(batch_job_json)
  return batch_job_json

async def get_batch_list_service():
  batch_jobs = client.batches.list()
  result= batch_jobs.to_dict()
  print(result)
  return  result

async def get_batch_status_service(batch_id: str):
  batch_job = client.batches.retrieve(batch_id)
  batch_job_dict = batch_job.to_dict()
  print(batch_job_dict)
  return batch_job_dict

async def get_batch_results_service(output_file_id: str):
  result = client.files.content(output_file_id).content
  print(result)
  result_file_name = "data/batch_job_results.jsonl"

  with open(result_file_name, 'wb') as file:
      file.write(result)

      # Loading data from saved file
  results = []
  with open(result_file_name, 'r') as file:
      for line in file:
          # Parsing the JSON string into a dict and appending to the list of results
          json_object = json.loads(line.strip())
          results.append(json_object)
  return results

async def save_sentences_from_batch_service():
  try:
    result_file_name = "data/batch_job_results.jsonl"
    words_data = {}
    with open(result_file_name, 'r') as file:
      for line in file:
        line_dict = json.loads(line)
        sentence = line_dict["response"]["body"]["choices"][0]["message"]["content"]
        custom_id = line_dict["custom_id"]
        user_id = custom_id.split("-")[0] 
        word = custom_id.split("-")[1]
        context = custom_id.split("-")[2]
        
        if user_id in words_data:
          words_data[user_id].append({"name": word, "context": context, "sentence": sentence})
        else:
          words_data[user_id] = [{"name": word, "context": context, "sentence": sentence}]

    for user_id in words_data:
      await create_sentence_service(user_id, words_data[user_id])
    return 'ok'
  except Exception as e:
    print("Error in saving sentences from batch service")
    raise INTERNAL_ERROR()
