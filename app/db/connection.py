import os

from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.getenv("DATA_BASE_URL")

engine: None | Engine = None

def get_engine() -> Engine:

    global engine

    if engine is None:
        engine = create_engine(
            url=DATA_BASE_URL,
            echo=True,
            future=True,
        )
    
    return engine

session = sessionmaker(
    bind=get_engine(),
    expire_on_commit=False,
    autoflush=False,
)

def get_session():
    try:
        db: Session = session()
        yield db
    finally:
        db.close()