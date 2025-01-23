#This file is used for making datamodels or table 
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
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
    ownner_id =  Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner = relationship("User") #build this relationship because from post table we can access user details for better readibility

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,server_default=text('now()')) 

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)