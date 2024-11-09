
from fastapi import FastAPI, APIRouter, HTTPException
from openai import OpenAI
from configurations import collection
from database.schemas import all_words
from database.models import Word
from bson.objectid import ObjectId
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

origins = ["*"]

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/word")
async def get_all_words():
    data = collection.find({},{"_id": 1, "name": 1, "context": 1} )
    result = []
    for word in data:
        result.append({
            "id": str(word["_id"]), 
            "name": word.get("name"),
            "context": word.get("context")
        })
    return result

@router.post("/word")
async def create_word(new_word : Word):
    try:
        resp = collection.insert_one(dict(new_word))
        print(resp)
        return {"status_code": 200, "id":str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error ocurred {e}")

@router.put("/word/{word_id}")
async def update_word(word_id: str, updated_word:Word):
    try:
        object_id = ObjectId(word_id)
        existing_doc = collection.find_one({"_id":object_id})
        if not existing_doc :
            return HTTPException(status_code=404, detail=f"Not found")
        collection.update_one({"_id":object_id}, {"$set":dict(updated_word)})
        updated_doc = collection.find_one({"_id": object_id})
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error ocurred {e}")
    return {"status_code": 200, "message":"word information has been updated",  "updated_document": updated_doc}

@router.get("/word/{word_id}")
async def get_word_by_id(word_id: str):
    try:
        object_id = ObjectId(word_id)
        document = collection.find_one({"_id": object_id})
        document["_id"] = str(document["_id"])
        if not document:
            raise HTTPException(status_code=404, detail="Word not found")
        return {"status_code": 200, "word": document}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

@router.delete("/word/{word_id}")
async def delete_word_by_id(word_id: str):
    try:
        object_id = ObjectId(word_id)
        delete_result = collection.delete_one({"_id": object_id})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Word not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    
    return {
        "status_code": 200,
        "message": "Word has been deleted successfully",
    }

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

@app.post("/generate_sentence/")
async def generate_sentence(word:Word):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not found")
    print(word)
    try:
        prompt = f"Create a not too long sentence in english using the word {word.name},consider sentence context is {word.context}"
        completion = client.chat.completions.create(
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

        sentence = completion.choices[0].message
        return {
            "status_code": 200,
            "result": sentence
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/send_batch")
def create_body():
    data = collection.find({},{"_id": 1, "name": 1, "context": 1} )
    requests = []
    for  word in data:
        custom_id = word.get("_id")
        name = word.get("name")
        context = word.get("context")
        word_obj = {
            "custom_id": f"sentence-{custom_id}",
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
    print(batch_file)
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    return {
        "status_code": 200,
        "result": batch_job
    }

@router.get("/check_batch_status/")
async def check_batch_status(batch_id: str):
    batch_job = client.batches.retrieve(batch_id)
    print(batch_job)
    return{
        "result": batch_job
    }

@router.get("/retrieving_batch/")
async def retrieving_batch(output_file_id: str):
    try:
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
        return {
            "status_code": 200,
            "result": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving batch status: {str(e)}")

app.include_router(router)