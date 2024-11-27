
from app.schemas.sentence_schema import GenerateSentenceSchemaInput
from app.openAPi.openAI_config import openAI

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

