from typing import Optional
from pydantic import BaseModel
from datetime import date


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
