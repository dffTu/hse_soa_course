from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from typing import Union
import httpx

from server.api import schemas
import server.config as config

router = APIRouter()


@router.post("/change_info", response_model=Union[None, schemas.ApiErrorResponse])
async def change_info(
    request: schemas.ChangeInfoRequest,
):
    response = httpx.post(url=config.USERS_SERVER_ADDR + "/change_info", content=request.model_dump_json())

    if response.status_code == 200:
        return Response(status_code=200)

    return JSONResponse(status_code=response.status_code, content=response.json())
