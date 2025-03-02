from fastapi import APIRouter

from . import register, auth

__all__ = ("router", "auth",)

router = APIRouter()
router.include_router(register.router, tags=["register"])
router.include_router(auth.router, tags=["auth"])
