from typing import Optional

from app.crud import UserCRUD
from app.models import User
from app.schemas import CreateUserSchema, UpdateUserSchema

from fastapi import Request


class UserAPI:
    @classmethod
    def get(cls, request: Request) -> Optional[User]:
        return UserCRUD(request.state.db_session).get_by_uuid(request.user.uuid)

    @classmethod
    def create(cls, request: Request, schema: CreateUserSchema) -> User:
        return UserCRUD(request.state.db_session).create(schema.dict())

    @classmethod
    def update(cls, request: Request, schema: UpdateUserSchema) -> User:
        return UserCRUD(request.state.db_session).update(
            request.user.uuid, schema.dict()
        )

    @classmethod
    def delete(cls, request: Request) -> None:
        return UserCRUD(request.state.db_session).delete_by_uuid(request.user.uuid)
