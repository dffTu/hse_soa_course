from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from server.api import schemas
from typing import Union

from db.main import users_db

router = APIRouter()


@router.post("/register", response_model=Union[None, schemas.ApiErrorResponse])
async def create_user(
    request: schemas.RegisterUserRequest,
):
    result = users_db.register_user(request.login, request.email, request.password)
    if result:
        return Response(status_code=200)
    else:
        response = schemas.ApiErrorResponse(
            exceptionMessage="User already registered!"
        )
        return JSONResponse(status_code=400, content=response.model_dump())
