from typing import Optional

from app.api.v1 import UserAPI
from app.dependencies.auth import login_required
from app.models import User
from app.schemas import CreateUserSchema, ReadUserSchema, UpdateUserSchema

from fastapi import APIRouter, Depends, Request

user_router = APIRouter()


@user_router.get(
    "/", response_model=ReadUserSchema, dependencies=[Depends(login_required)]
)
async def get(request: Request) -> Optional[User]:
    return UserAPI.get(request)


@user_router.post("/", response_model=ReadUserSchema)
async def create(request: Request, schema: CreateUserSchema) -> User:
    return UserAPI.create(request, schema)


@user_router.put(
    "/", response_model=ReadUserSchema, dependencies=[Depends(login_required)]
)
async def update(request: Request, schema: UpdateUserSchema) -> User:
    return UserAPI.update(request, schema)


@user_router.delete("/", dependencies=[Depends(login_required)])
async def delete(request: Request) -> None:
    return UserAPI.delete(request)
