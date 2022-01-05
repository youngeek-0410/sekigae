from typing import Optional
from uuid import UUID

from app.db.database import get_db_session
from app.models import User
from sqlalchemy.orm import scoped_session

from ..core.exceptions import (
    ApiException,
    FirebaseUidOrPasswordMustBeSet,
    NotFoundObjectMatchingUuid,
    create_error,
)
from ..core.security import get_password_hash
from .base import BaseCRUD

db_session = get_db_session()


class UserCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, User)

    def create(self, data: dict = {}) -> User:
        # FIXME: セキュリティ的に、そのメールアドレスのユーザーが存在することを伝えるのはよくない?
        if self.get_query().filter_by(email=data["email"]).first():
            raise ApiException(
                create_error(f"User with email {data['email']} already exists")
            )
        if data["password"] is not None:
            password = data.pop("password")
            data["hashed_password"] = get_password_hash(password)
            return super().create(data)
        elif data["firebase_uid"] is not None:
            return super().create(data)
        else:
            raise ApiException(FirebaseUidOrPasswordMustBeSet)

    def update(self, uuid: UUID, data: dict = {}) -> User:
        # FIXME: セキュリティ的に、そのメールアドレスのユーザーが存在することを伝えるのはよくない?
        update_obj = self.get_by_uuid(uuid)
        if update_obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(self.model, uuid))
        new_data_obj = self.get_query().filter_by(email=data["email"]).first()
        if new_data_obj is not None and new_data_obj.uuid != update_obj.uuid:
            raise ApiException(
                create_error(f"User with email {data['email']} already exists")
            )
        if data["password"] is not None:
            password = data.pop("password")
            data["hashed_password"] = get_password_hash(password)
            return super().update(uuid, data)
        elif data["firebase_uid"] is not None:
            return super().update(uuid, data)
        else:
            raise ApiException(FirebaseUidOrPasswordMustBeSet)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_query().filter_by(email=email).first()
