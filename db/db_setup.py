from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
import os

import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("cannot fetch DATABASE_URL from .env.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(
    DATABASE_URL, future=True, 
)

SessionLocal= sessionmaker(
    autoflush=False, autocommit=False, bind=engine, future=True
)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error occured during DB operation: {e}")
        raise e
    finally:
        db.close()