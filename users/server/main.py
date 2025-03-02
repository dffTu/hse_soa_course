import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response

from server import config
from server.api import router

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    logger.exception("Invalid request data: %s", exc)
    return await request_validation_exception_handler(request, exc)

app = FastAPI(
    title="users",
)

app.exception_handler(RequestValidationError)(validation_exception_handler)

app.include_router(router=router)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    uvicorn.run(
        app,
        host=config.SERVER_IP,
        port=config.PORT,
        log_level=os.getenv("LOGGING_LEVEL", "info").lower(),
    )