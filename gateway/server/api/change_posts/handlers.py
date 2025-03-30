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
