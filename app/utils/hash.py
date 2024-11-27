import os
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
ACCESS_ALGORITHM = os.getenv("ACCESS_ALGORITHM")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ACCESS_ALGORITHM)
