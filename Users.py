from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import HTTPException,status,Depends
import time
from . import models
from .models import Post as PostModelDB
from typing import Optional,List
from .ORM import engine,get_db
from sqlalchemy.orm import Session
from .schema import UpdatingPost,CreatePost,ApiResponsetoUser,UserValidation,CreatedUserResponse
models.Base.metadata.create_all(bind = engine) # this line creates table which is refer to it right after runing the code if table is not there and it also use to communicate with tables

app = FastAPI()


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=CreatedUserResponse)
def create_user(user: UserValidation,db:Session = Depends(get_db)):
    new_User = models.User(**user.dict())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User
    