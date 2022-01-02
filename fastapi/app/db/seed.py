from logging import getLogger

from app.crud import UserCRUD
from app.db.database import get_db_session
from app.schemas import CreateUserSchema

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


def seed_all():
    from .data import USERS

    logger.info("Seeding data...")
    seed_users(USERS)
    logger.info("done")
