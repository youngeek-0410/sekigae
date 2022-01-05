from uuid import UUID

from app.models import Student
from pydantic import BaseModel, Field


class BaseStudentSchema(BaseModel):
    name: str = Field(..., max_length=Student.MAX_LENGTH_NAME)
    number: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class CreateStudentSchema(BaseStudentSchema):
    student_sheet_uuid: UUID


class UpdateStudentSchema(BaseStudentSchema):
    student_sheet_uuid: UUID


class CreateFormStudentSchema(BaseStudentSchema):
    pass


class UpdateFormStudentSchema(BaseStudentSchema):
    pass


class ReadStudentSchema(BaseStudentSchema):
    uuid: UUID
