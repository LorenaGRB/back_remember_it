from fastapi.responses import JSONResponse
from typing import Any, Dict

def SUCCESS_RESPONSE(message: str = "Operation successful", data: Any = None) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": message,
            "data": data,
        },
    )

def CREATED_RESPONSE(message: str = "Resource created successfully", data: dict = None) -> JSONResponse:
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": message,
            "data": data,
        },
    )
