from sqlalchemy import VARCHAR, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from .base import BaseModelMixin


class StudentSheet(BaseModelMixin):
    __tablename__ = "student_sheets"
    __table_args__ = UniqueConstraint("name", "user_uuid"), {}

    MAX_LENGTH_NAME = 100
    name = Column(VARCHAR(MAX_LENGTH_NAME), nullable=False)

    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    students = relationship("Student", backref="student_sheet", cascade="all")
