import re
from app.utils.exceptions import BAD_REQUEST

def validate_password(password: str):
    if not password:
        raise BAD_REQUEST("Password is required")
    if len(password) < 8:
        raise BAD_REQUEST( "Password must be at least 8 characters long")

def validate_email(email: str):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        raise BAD_REQUEST("Invalid email format")

def validate_user_creation(user_data: dict):
    if not user_data.get("username"):
        raise BAD_REQUEST("Username is required")
    if not user_data.get("email"):
        raise BAD_REQUEST("Email is required")
    if not user_data.get("pwd"):
        raise BAD_REQUEST("Password is required")
    
    validate_password(user_data["pwd"])
    validate_email(user_data["email"])

