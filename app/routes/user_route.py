from fastapi import APIRouter, Depends
from app.schemas.user_schema import LoginResponse, SaveUserTokenInput, UserSchema, UserResponse, UserToLogin
from app.services.user_service import get_all_users, add_user, login, save_user_token_service,get_mobile_token_service
from app.middlewares.auth import AuthenticationMiddleware

router = APIRouter()
auth  = AuthenticationMiddleware()

@router.get("/", dependencies = [Depends(auth)])
async def get_users():
  return await get_all_users()

@router.post("/", dependencies = [Depends(auth)])
async def create_user(user: UserSchema):
  return await add_user(user)

@router.post("/login")
async def login_user(user: UserToLogin):
  return await login(user)

@router.post("/token", dependencies = [Depends(auth)])
async def save_user_token(token_info:SaveUserTokenInput):
  return await save_user_token_service(token_info)

@router.get("/token", dependencies = [Depends(auth)])
async def get_mobile_token(user_id: str):
  return await get_mobile_token_service(user_id)