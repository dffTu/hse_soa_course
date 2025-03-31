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

@router.get("/get_posts", response_model=Union[schemas.GetPostsPagedResponse, schemas.ApiErrorResponse])
async def get_posts(
    request: Request,
    get_posts_request: schemas.GetPostsPagedRequest
):
    if get_posts_request.page < 1 or get_posts_request.page_size < 1:
        response = schemas.ApiErrorResponse(exceptionMessage='page and page_size should be > 1!')
        return JSONResponse(status_code=404, content=response.model_dump())
    response = request.app.grpc_client.get_posts_pages(get_posts_request)
    return response
