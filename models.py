#This file is used for making datamodels or table 
from sqlalchemy import Column,Integer,String,Boolean
from .ORM import Base

class Post(Base):
    __table__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published =Column(Boolean,default=True)
    rating = Column(Integer,nullable=False)