from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("openai key not exist")

openAI = OpenAI()
