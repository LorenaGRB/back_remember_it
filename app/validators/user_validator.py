from fastapi import HTTPException
import re

def validate_password(password: str):
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )

def validate_email(email: str):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

def validate_user_creation(user_data: dict):
    if not user_data.get("username"):
        raise HTTPException(status_code=400, detail="Username is required")
    if not user_data.get("email"):
        raise HTTPException(status_code=400, detail="Email is required")
    if not user_data.get("pwd"):
        raise HTTPException(status_code=400, detail="Password is required")
    
    validate_password(user_data["pwd"])
    validate_email(user_data["email"])
