from app.api.v1.auth import AuthAPI
from app.schemas.auth import PaswordLoginSchema

from fastapi import APIRouter, Depends, Request

auth_router = APIRouter()


@auth_router.post("/login/password")
async def password_login(request: Request, schema: PaswordLoginSchema = Depends()):
    return AuthAPI.password_login(request, schema)
