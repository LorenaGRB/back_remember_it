from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema, UserResponse
from app.services.user_service import get_all_users, add_user

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users():
    return await get_all_users()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserSchema):
    return await add_user(user)
