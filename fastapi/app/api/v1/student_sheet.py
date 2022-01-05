from typing import List, Optional
from uuid import UUID

from app.core.exceptions import (
    ApiException,
    NotFoundObjectMatchingUuid,
    PermissionDenied,
)
from app.crud import StudentSheetCRUD
from app.models import StudentSheet
from app.schemas import (
    CreateFormStudentSheetSchema,
    CreateStudentSheetSchema,
    UpdateFormStudentSheetSchema,
    UpdateStudentSheetSchema,
)

from fastapi import Request


class StudentSheetAPI:
    @classmethod
    def gets(cls, request: Request) -> List[StudentSheet]:
        return StudentSheetCRUD(request.state.db_session).gets_by_user_uuid(
            request.user.uuid
        )

    @classmethod
    def get(cls, request: Request, uuid: UUID) -> Optional[StudentSheet]:
        obj = StudentSheetCRUD(request.state.db_session).get_by_uuid(uuid)
        if obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(StudentSheet, uuid))
        if obj.user_uuid != request.user.uuid:
            raise ApiException(PermissionDenied())
        return obj

    @classmethod
    def create(
        cls, request: Request, schema: CreateFormStudentSheetSchema
    ) -> StudentSheet:
        data = CreateStudentSheetSchema(user_uuid=request.user.uuid, **schema.dict())
        return StudentSheetCRUD(request.state.db_session).create(data)

    @classmethod
    def update(
        cls, request: Request, uuid: UUID, schema: UpdateFormStudentSheetSchema
    ) -> StudentSheet:
        obj = StudentSheetCRUD(request.state.db_session).get_by_uuid(uuid)
        if not obj:
            raise ApiException(NotFoundObjectMatchingUuid(StudentSheet, uuid))
        if obj.user_uuid != request.user.uuid:
            raise ApiException(PermissionDenied)
        data = UpdateStudentSheetSchema(user_uuid=request.user.uuid, **schema.dict())
        return StudentSheetCRUD(request.state.db_session).update(uuid, data)

    @classmethod
    def delete(cls, request: Request, uuid: UUID) -> None:
        obj = StudentSheetCRUD(request.state.db_session).get_by_uuid(uuid)
        if not obj:
            raise ApiException(NotFoundObjectMatchingUuid(StudentSheet, uuid))
        if obj.user_uuid != request.user.uuid:
            raise ApiException(PermissionDenied)
        return StudentSheetCRUD(request.state.db_session).delete_by_uuid(uuid)
