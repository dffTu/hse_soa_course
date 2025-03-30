from fastapi import APIRouter

from . import register, auth, change_info, change_posts

__all__ = ("router",)

router = APIRouter()
router.include_router(register.router, tags=["register"])
router.include_router(auth.router, tags=["auth"])
router.include_router(change_info.router, tags=["change_info"])
router.include_router(change_posts.router, tags=["change_posts"])
