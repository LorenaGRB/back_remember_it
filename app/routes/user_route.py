from fastapi import APIRouter
from app.schemas.user_schema import LoginResponse, UserSchema, UserResponse, UserToLogin
from app.services.user_service import get_all_users, add_user, login

router = APIRouter()

@router.get("/")
async def get_users():
    return await get_all_users()

@router.post("/")
async def create_user(user: UserSchema):
    return await add_user(user)

@router.post("/login")
async def login_user(user: UserToLogin):
     return await login(user)
