from fastapi import APIRouter
from fastapi.responses import JSONResponse
from server.api import schemas
from typing import Union

from db.main import users_db

router = APIRouter()


@router.post("/auth", response_model=Union[schemas.SuccesfulAuthResponse, schemas.ApiErrorResponse])
async def auth_user(
    request: schemas.AuthUserRequest,
):
    token = users_db.auth_user(request.login, request.password)
    if token is not None:
        response = schemas.SuccesfulAuthResponse(
            token=token
        )
        return JSONResponse(status_code=200, content=response.model_dump())
    else:
        response = schemas.ApiErrorResponse(
            exceptionMessage="User with this password not found!"
        )
        return JSONResponse(status_code=400, content=response.model_dump())
