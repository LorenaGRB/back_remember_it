from fastapi import HTTPException

def BAD_REQUEST(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)

def NOT_FOUND(detail: str = "Resource not found"):
    raise HTTPException(status_code=404, detail=detail)

def UNAUTHORIZED(detail: str = "Unauthorized access"):
    raise HTTPException(status_code=401, detail=detail)

def FORBIDDEN(detail: str = "Forbidden access"):
    raise HTTPException(status_code=403, detail=detail)

def INTERNAL_ERROR(detail: str = "Internal server error"):
    raise HTTPException(status_code=500, detail=detail)
