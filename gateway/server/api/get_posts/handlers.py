from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Union

from server.api import schemas

router = APIRouter()


@router.get("/get_post/{post_id}", response_model=Union[schemas.Post, schemas.ApiErrorResponse])
async def get_post(
    request: Request,
    post_id: int
):
    response = request.app.grpc_client.get_post(post_id)
    if isinstance(response, schemas.ApiErrorResponse):
        return JSONResponse(status_code=404, content=response.model_dump())
    return response
