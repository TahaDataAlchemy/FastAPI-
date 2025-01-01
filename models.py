#This file is used for making datamodels or table 
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .ORM import Base

class Post(Base):
    #you cannot modify tables when created using sqlalchemy if you need to add some thing do it before the table is created, the sql alchemy sees if table is there it wont go further to see changes in it 
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published =Column(Boolean,server_default='TRUE',nullable=False)
    rating = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,server_default=text('now()')) 
