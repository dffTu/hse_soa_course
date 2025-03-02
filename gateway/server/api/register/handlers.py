from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from typing import Union
import httpx

from server.api import schemas
import server.config as config

router = APIRouter()


@router.post("/register", response_model=Union[None, schemas.ApiErrorResponse])
async def register_user(
    request: schemas.RegisterUserRequest,
):
    response = httpx.post(url=config.USERS_SERVER_ADDR + "/register", content=request.model_dump_json())

    if response.status_code == 200:
        return Response(status_code=200)

    return JSONResponse(status_code=response.status_code, content=response.json())
