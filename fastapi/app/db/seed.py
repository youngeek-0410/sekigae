from logging import getLogger

from app.db.database import get_db_session

logger = getLogger(__name__)

db_session = get_db_session()


def seed_all():
    logger.info("Seeding data...")
    logger.info("done")
