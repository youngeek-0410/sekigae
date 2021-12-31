from typing import Optional
from uuid import UUID

from app.models import User
from pydantic import BaseModel, Field


class BaseUserSchema(BaseModel):
    email: str = Field(..., regex=r"[^\s]+@[^\s]+")

    class Config:
        orm_mode = True


class CreateUserSchema(BaseUserSchema):
    password: Optional[str] = Field(None, min_length=User.MIN_LENGTH_PASSWORD)


class UpdateUserSchema(BaseUserSchema):
    password: Optional[str] = Field(None, min_length=User.MIN_LENGTH_PASSWORD)


class ReadUserSchema(BaseUserSchema):
    uuid: UUID


class ReadSimpleUserSchema(BaseUserSchema):
    uuid: UUID


class ReadUserForOtherUserSchema(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True
