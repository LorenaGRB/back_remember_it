from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGO_URL:str
    DB_NAME: str

    class Config:
        env_file = "./env"

settings = Settings()