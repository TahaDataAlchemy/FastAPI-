from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # establishing connection db
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine) # this session is used for talking to database and the values inside it are default 

Base = declarative_base() #use for making table in db 