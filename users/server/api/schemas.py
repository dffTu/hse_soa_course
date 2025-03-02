from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    login: str
    password: str
    email: str


class AuthUserRequest(BaseModel):
    login: str
    password: str


class SuccesfulAuthResponse(BaseModel):
    token: str

class ApiErrorResponse(BaseModel):
    exceptionMessage: str
