from typing import Optional
from uuid import UUID

from app.db.database import get_db_session
from app.models import User
from sqlalchemy.orm import scoped_session

from ..core.security import get_password_hash
from .base import BaseCRUD

db_session = get_db_session()


class UserCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, User)

    def create(self, data: dict = {}) -> User:
        data["hashed_password"] = get_password_hash(data.pop("password"))
        return super().create(data)

    def update(self, uuid: UUID, data: dict = {}) -> User:
        data["hashed_password"] = get_password_hash(data.pop("password"))
        return super().update(uuid, data)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_query().filter_by(email=email).first()
