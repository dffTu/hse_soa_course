from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class RegisterUserRequest(BaseModel):
    login: str
    password: str
    email: str


class AuthUserRequest(BaseModel):
    login: str
    password: str


class ChangeInfoRequest(BaseModel):
    token: str
    name: Optional[str]
    surname: Optional[str]
    birthday: Optional[date]
    email: Optional[str]
    phone_number: Optional[str]
    city: Optional[str]


class SuccesfulAuthResponse(BaseModel):
    token: str

class ApiErrorResponse(BaseModel):
    exceptionMessage: str


class Post(BaseModel):
    name: str
    description: str
    author_id: int
    is_private: bool
    tags: list[str]
    created_at: datetime
    updated_at: datetime

class CreatePostRequest(BaseModel):
    name: str
    description: str
    author_id: int
    is_private: bool
    tags: list[str]

class CreatePostResponse(BaseModel):
    post_id: int

class UpdatePostRequest(BaseModel):
    post_id: int
    post: Post

class DeletePostRequst(BaseModel):
    post_id: int

class GetPostRequest(BaseModel):
    post_id: int

class GetPostsPagedRequest(BaseModel):
    page: int
    page_size: int

class GetPostsPagedResponse(BaseModel):
    posts: list[Post]
    page: int
    total_pages: int
    total_posts: int
