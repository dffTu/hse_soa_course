from fastapi import APIRouter

from . import register

__all__ = ("router",)

router = APIRouter()
router.include_router(register.router, tags=["register"])
