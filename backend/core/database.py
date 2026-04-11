"""Stuff for the database management."""
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from .utilities import find_project_root

logger = logging.getLogger(__name__)

load_dotenv()

ENV = os.getenv("ENVIRONMENT")
if ENV == "prod":
    DB_USER = required_env("POSTGRES_USER")
    DB_PASSWORD = required_env("POSTGRES_PASSWORD")
    DB_NAME = required_env("POSTGRES_DB")
    DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", default = 5555)

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Create the SQLAlchemy engine
    
elif ENV == "dev":
    DATABASE_URL = f"sqlite:///{find_project_root()}/mydb.db"

logger.debug("DATABASE_URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()