from sqlalchemy import BOOLEAN, VARCHAR, Column, String
from sqlalchemy.orm import relationship

from .base import BaseModelMixin


class User(BaseModelMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    MIN_LENGTH_PASSWORD = 8
    hashed_password = Column(String, nullable=True)

    MAX_LENGTH_FIREBASE_UID = 128
    firebase_uid = Column(VARCHAR(MAX_LENGTH_FIREBASE_UID), unique=True, nullable=True)

    is_admin = Column(BOOLEAN, nullable=False, default=False)

    student_sheets = relationship("StudentSheet", backref="user", cascade="all")
