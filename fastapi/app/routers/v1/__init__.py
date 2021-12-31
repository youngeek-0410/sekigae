from fastapi import APIRouter

from .auth import auth_router
from .user import user_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
