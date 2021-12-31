from app.core.settings import get_env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL: str = get_env().db_url

engine = create_engine(DATABASE_URL, echo=True)
local_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = local_session.query_property()


def get_db_session() -> scoped_session:
    return local_session
