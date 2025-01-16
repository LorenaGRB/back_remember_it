from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema, UserToLogin
from app.utils.exceptions import NOT_FOUND, UNAUTHORIZED
from app.utils.hash import create_access_token, hash_password, verify_password
from app.validators.user_validator import validate_user_creation

user_repo = UserRepository()

async def get_all_users():
    return await user_repo.get_all_users()

async def add_user(user_data: UserSchema):
    user = dict(user_data)
    validate_user_creation(user)
    print(user_data.pwd)
    user["pwd"] = hash_password(user_data.pwd)
    created_user = await user_repo.add_user(user)
    return created_user

async def get_user_by_id(user_id: str):
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise NOT_FOUND(detail="User not found")
    return user

async def delete_user(user_id: str):
    success = await user_repo.delete_user(user_id)
    if not success:
        raise NOT_FOUND(detail="User not found")
    return {"detail": "User deleted successfully"}

async def update_user(user_id: str, update_data: dict):
    success = await user_repo.update_user(user_id, update_data)
    if not success:
        raise NOT_FOUND(detail="User not found")
    return {"detail": "User updated successfully"}

async def login(user: UserToLogin):
    saved_user = await user_repo.get_user_by_username(user.username)
    if not saved_user:
        raise NOT_FOUND(detail="User not found")
    current_user = dict(user)
    saved_pwd = saved_user["pwd"]
    current_pwd = current_user["pwd"]
    is_verified = verify_password(current_pwd,saved_pwd)
    if not is_verified:
        raise UNAUTHORIZED()
    token_username={"id": saved_user["id"], "username": saved_user["username"]}
    access_token = create_access_token(token_username)
    user_id = saved_user["id"]
    username = saved_user["username"]
    return { "token": str(access_token), "id": user_id, "username": username}

async def save_user_token_service(token_info):
    return await user_repo.save_user_token_repository(token_info)

async def get_mobile_token_service(user_id: str):
    return await user_repo.get_mobile_token_repository(user_id)