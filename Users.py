from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import HTTPException,status,Depends
import time
from . import models
from .models import Post as PostModelDB,User
from typing import Optional,List
from .ORM import engine,get_db
from sqlalchemy.orm import Session
from .schema import UpdatingPost,CreatePost,ApiResponsetoUser,UserValidation,CreatedUserResponse
from . import utils
models.Base.metadata.create_all(bind = engine) # this line creates table which is refer to it right after runing the code if table is not there and it also use to communicate with tables

app = FastAPI()


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=CreatedUserResponse)
def create_user(user: UserValidation,db:Session = Depends(get_db)):

    existingUser  = db.query(models.User).filter(models.User.email == user.email).first()
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "A user witht this email already Exist"
        )
    hashed_password = utils.hashpass(user.password)
    user.password = hashed_password

    new_User = models.User(**user.dict())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User

@app.get('/users/{id}',status_code=status.HTTP_200_OK,response_model = CreatedUserResponse)
def get_users(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "User With this Id Not Exist"
        )
    return user