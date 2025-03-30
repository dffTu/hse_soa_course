from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from typing import Union
import httpx

from server.api import schemas
import server.config as config

router = APIRouter()


@router.post("/change_posts", response_model=schemas.CreatePostResponse)
async def create_post(
    request: Request,
    post: schemas.CreatePostRequest,
):
    return request.app.grpc_client.create_post(post)

@router.patch("/change_posts", response_model=Union[schemas.Post, schemas.ApiErrorResponse])
async def update_post(
    request: Request,
    post: schemas.UpdatePostRequest,
):
    response = request.app.grpc_client.update_post(post)
    if isinstance(response, schemas.ApiErrorResponse):
        return JSONResponse(status_code=404, content=response.model_dump())
    return request.app.grpc_client.update_post(post)
