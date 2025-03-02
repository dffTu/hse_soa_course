from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Union
import httpx

from server.api import schemas
import server.config as config

router = APIRouter()


@router.post("/auth", response_model=Union[schemas.SuccesfulAuthResponse, schemas.ApiErrorResponse])
async def auth_user(
    request: schemas.AuthUserRequest,
):
    response = httpx.post(url=config.USERS_SERVER_ADDR + "/auth", content=request.model_dump_json())

    return JSONResponse(status_code=response.status_code, content=response.json())
