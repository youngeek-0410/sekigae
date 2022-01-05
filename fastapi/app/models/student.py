from sqlalchemy import INTEGER, VARCHAR, CheckConstraint, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from .base import BaseModelMixin


class Student(BaseModelMixin):
    __tablename__ = "students"

    MAX_LENGTH_NAME = 100
    name = Column(VARCHAR(MAX_LENGTH_NAME), nullable=False)

    number = Column(INTEGER, nullable=False)

    student_sheet_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("student_sheets.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("number", "student_sheet_uuid"),
        CheckConstraint(number > 0),
    )
