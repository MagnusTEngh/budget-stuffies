"""To run this, run the command 'uv run python -m backend.db.init_db' from project root"""

import logging
import os

from dotenv import load_dotenv
from .base import Base
from ..core.database import engine

from ..modules.transactions import models

logger = logging.getLogger(__name__)
load_dotenv()


def establish_prod_database():
    uvlogger.info("Creating prod database...")
    Base.metadata.create_all(engine)
    logger.info("Tables created successfully!")


def establish_test_database():
    logger.info("Creating dev database...")
    Base.metadata.create_all(engine)
    logger.info("Tables created successfully!")
    from sqlalchemy.orm import Session
    from ..modules.transactions.test_data import testdata_transactions
    with Session(engine) as session:
        session.add_all([x.to_orm() for x in testdata_transactions])
        session.commit()


if __name__ == "__main__":
    ENV = os.getenv("ENVIRONMENT")
    if ENV == "prod":
        establish_prod_database()
    elif ENV == "dev":
        establish_test_database()
    else:
        raise ValueError(
            ".env file should contain an 'ENVIRONMENT' variable that is either 'prod' or 'dev'"
        )
