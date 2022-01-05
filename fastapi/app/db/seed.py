from logging import getLogger

from app.crud import StudentSheetCRUD, UserCRUD
from app.db.database import get_db_session
from app.schemas import CreateStudentSheetSchema, CreateUserSchema

logger = getLogger(__name__)

db_session = get_db_session()


def seed_users(users):
    for user in users:
        if not UserCRUD(db_session).get_by_email(user["email"]):
            user_schema = CreateUserSchema(
                email=user["email"],
                password=user["password"],
            )
            created_user = UserCRUD(db_session).create(user_schema.dict())
            logger.info(f"Created user: {created_user.email}")
        else:
            logger.info(f"Skipped user: {user['email']}")
    db_session.commit()


def seed_student_sheets(student_sheets):
    for student_sheet in student_sheets:
        user = UserCRUD(db_session).get_by_email(student_sheet["user"]["email"])
        assert user is not None
        if not StudentSheetCRUD(db_session).get_by_user_uuid_and_name(
            user.uuid, student_sheet["name"]
        ):
            student_sheet_schema = CreateStudentSheetSchema(
                name=student_sheet["name"], user_uuid=user.uuid
            )
            StudentSheetCRUD(db_session).create(student_sheet_schema)
            logger.info(f"Created student sheet: {student_sheet['name']}")
        else:
            logger.info(f"Skipped student sheet: {student_sheet['name']}")
    db_session.commit()


def seed_all():
    from .data import STUDENT_SHEETS, USERS

    logger.info("Seeding data...")
    seed_users(USERS)
    seed_student_sheets(STUDENT_SHEETS)
    logger.info("done")
