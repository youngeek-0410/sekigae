from sqlalchemy import BOOLEAN, Column, String

from .base import BaseModelMixin


class User(BaseModelMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    MIN_LENGTH_PASSWORD = 8
    hashed_password = Column(String, nullable=True)

    is_admin = Column(BOOLEAN, nullable=False, default=False)
