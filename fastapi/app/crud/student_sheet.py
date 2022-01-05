from typing import List, Optional
from uuid import UUID

from app.core.exceptions import ApiException, NotFoundObjectMatchingUuid, create_error
from app.db.database import get_db_session
from app.models import StudentSheet
from app.schemas import CreateStudentSheetSchema, UpdateStudentSheetSchema
from sqlalchemy.orm import scoped_session

from .base import BaseCRUD

db_session = get_db_session()


class StudentSheetCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, StudentSheet)

    def gets_by_user_uuid(self, user_uuid: UUID) -> List[StudentSheet]:
        return self.get_query().filter_by(user_uuid=user_uuid).all()

    def get_by_user_uuid_and_name(
        self, user_uuid: UUID, name: str
    ) -> Optional[StudentSheet]:
        return self.get_query().filter_by(user_uuid=user_uuid, name=name).first()

    def create(self, schema: CreateStudentSheetSchema) -> StudentSheet:
        if self.get_by_user_uuid_and_name(schema.user_uuid, schema.name) is not None:
            raise ApiException(
                create_error(f"StudentSheet with name {schema.name} already exists")
            )
        return super().create(schema.dict())

    def update(self, uuid: UUID, schema: UpdateStudentSheetSchema) -> StudentSheet:
        update_obj = self.get_by_uuid(uuid)
        if update_obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(self.model, uuid))

        new_data_obj = self.get_by_user_uuid_and_name(schema.user_uuid, schema.name)
        if new_data_obj is not None and new_data_obj.uuid != update_obj.uuid:
            raise ApiException(
                create_error(f"StudentSheet with name {schema.name} already exists")
            )
        return super().update(uuid, schema.dict())
