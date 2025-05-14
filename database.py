from os import getenv
from sqlmodel import SQLModel, create_engine


SQLMODEL_DATABASE_URL = getenv("SQLMODEL_DATABASE_URL")
if not SQLMODEL_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

SQLMODEL_ECHO = getenv("SQLMODEL_ECHO", "false").lower() == "true"

engine = create_engine(SQLMODEL_DATABASE_URL, echo=SQLMODEL_ECHO)


def init_database():
    """
    Initialize the database by creating all tables.
    """
    import models  # noqa: F401

    SQLModel.metadata.create_all(engine)
