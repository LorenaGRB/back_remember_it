from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_service import verify_token

class AuthenticationMiddleware(HTTPBearer):
    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        return verify_token(token)
