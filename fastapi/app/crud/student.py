from typing import List, Optional
from uuid import UUID

from app.core.exceptions import ApiException, NotFoundObjectMatchingUuid, create_error
from app.db.database import get_db_session
from app.models import Student
from app.schemas import CreateStudentSchema, UpdateStudentSchema
from sqlalchemy.orm import scoped_session

from .base import BaseCRUD

db_session = get_db_session()


class StudentCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, Student)

    def gets_by_student_sheet_uuid(self, student_sheet_uuid: UUID) -> List[Student]:
        return self.get_query().filter_by(student_sheet_uuid=student_sheet_uuid).all()

    def get_by_student_sheet_uuid_and_number(
        self, student_sheet_uuid: UUID, number: int
    ) -> Optional[Student]:
        return (
            self.get_query()
            .filter_by(student_sheet_uuid=student_sheet_uuid, number=number)
            .first()
        )

    def create(self, schema: CreateStudentSchema) -> Student:
        if (
            self.get_by_student_sheet_uuid_and_number(
                schema.student_sheet_uuid, schema.number
            )
            is not None
        ):
            raise ApiException(
                create_error(
                    f"Student with number {schema.number} already exists in this student sheet."
                )
            )
        return super().create(schema.dict())

    def update(self, uuid: UUID, schema: UpdateStudentSchema) -> Student:
        update_obj = self.get_by_uuid(uuid)
        if update_obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(self.model, uuid))

        new_data_obj = self.get_by_student_sheet_uuid_and_number(
            schema.student_sheet_uuid, schema.number
        )
        if new_data_obj is not None and new_data_obj.uuid != update_obj.uuid:
            raise ApiException(
                create_error(
                    f"Student with number {schema.number} already exists in this student sheet."
                )
            )
        return super().update(uuid, schema.dict())
