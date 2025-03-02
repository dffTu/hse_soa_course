from fastapi import APIRouter

from . import register, auth, change_info

__all__ = ("router",)

router = APIRouter()
router.include_router(register.router, tags=["register"])
router.include_router(auth.router, tags=["auth"])
router.include_router(change_info.router, tags=["change_info"])
