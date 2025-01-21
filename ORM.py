from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL) # establishing connection db
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine) # this session is used for talking to database and the values inside it are default 

Base = declarative_base() #use for making table in db 

#We using it to contact with db tables and every time we send api request to db or giv sql statment it made session and execute, after close the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()