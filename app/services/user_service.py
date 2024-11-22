from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema
from app.utils.hash import hash_password
from app.validators.user_validator import validate_user_creation

user_repo = UserRepository()

async def get_all_users():
    return await user_repo.get_all_users()

async def add_user(user_data: UserSchema):
    user = dict(user_data)
    validate_user_creation(user)
    user["pwd"] = hash_password(user_data.pwd)
    created_user = await user_repo.add_user(user)
    return created_user

async def get_user_by_id(user_id: str):
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def delete_user(user_id: str):
    success = await user_repo.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

async def update_user(user_id: str, update_data: dict):
    success = await user_repo.update_user(user_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User updated successfully"}
