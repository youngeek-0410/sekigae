from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.settings import get_env
from app.models import StudentSheet
from pydantic import BaseModel, Field, validator

from .user import ReadUserSchema


class BaseStudentSheetSchema(BaseModel):
    name: str = Field(..., max_length=StudentSheet.MAX_LENGTH_NAME)

    class Config:
        orm_mode = True


class CreateStudentSheetSchema(BaseStudentSheetSchema):
    user_uuid: UUID


class UpdateStudentSheetSchema(BaseStudentSheetSchema):
    user_uuid: UUID


class CreateFormStudentSheetSchema(BaseStudentSheetSchema):
    pass


class UpdateFormStudentSheetSchema(BaseStudentSheetSchema):
    pass


class ReadStudentSheetSchema(BaseStudentSheetSchema):
    uuid: UUID
    user: ReadUserSchema
    created_at: datetime
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def convert_to_default_timezone(
        cls, value: Optional[datetime]
    ) -> Optional[datetime]:
        return value and value.astimezone(get_env().default_timezone)
