from fastapi import APIRouter

from .auth import auth_router
from .studnet_sheet import student_sheet_router
from .user import user_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(
    student_sheet_router, prefix="/student-sheets", tags=["student sheets"]
)
