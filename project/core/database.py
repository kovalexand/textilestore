from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.core.config import get_db_settings

settings = get_db_settings()
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.username}:{settings.password}@"
    f"{settings.host}:{settings.port}/{settings.database}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
