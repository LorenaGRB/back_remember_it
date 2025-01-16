from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os 

SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')

def create_access_token(data:dict):
  payload = data.copy()
  token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
  return token

def verify_token(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return payload
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token is expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token")
    