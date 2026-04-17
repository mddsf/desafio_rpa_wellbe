from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL)

def get_session():
    return Session(engine)