from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from server.api import schemas
from typing import Union

from db.main import users_db

router = APIRouter()


@router.post("/change_info", response_model=Union[None, schemas.ApiErrorResponse])
async def change_info(
    request: schemas.ChangeInfoRequest,
):
    result = users_db.change_user_info(
        request.token,
        request.name,
        request.surname,
        request.birthday,
        request.email,
        request.phone_number,
        request.city
    )
    if result:
        return Response(status_code=200)
    else:
        response = schemas.ApiErrorResponse(
            exceptionMessage="Token not found!"
        )
        return JSONResponse(status_code=404, content=response.model_dump())
