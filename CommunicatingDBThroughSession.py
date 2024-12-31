from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException,status,Depends
import time
from . import models
from .models import Post as PostModelDB
from .ORM import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine) # this line creates table which is refer to it right after runing the code if table is not there and it also use to communicate with tables

app = FastAPI()


#Validating Our Model
class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None #its optional if not a value no problem None will return




@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status":"success"}

#Use to retrieve All Post present in Memory
@app.get("/DBposts",status_code=status.HTTP_200_OK)
def get_Db_Post(db: Session = Depends(get_db)):
    posts = db.query(PostModelDB).all()
    return {"data":posts}

@app.post("/creatingPost",status_code=status.HTTP_201_CREATED)
def PostCreated(post:Post,db:Session = Depends(get_db)):
    new_post = PostModelDB(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #Refresh to get generated Fields
    return {"data":new_post}

@app.get("/DBposts/{id}",status_code=status.HTTP_200_OK)
def getSinglePost(id: int,db:Session = Depends(get_db)):
    post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} is not Found"
        )
    return {"data":post}

@app.delete("/DBposts/{id}",status_code=status.HTTP_200_OK)
def deletingSimplePostFromDB(id: int,db:Session = Depends(get_db)):
    deleted_post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post With ID {id} does not Exist"
        )
    db.delete(deleted_post)
    db.commit()
    return {
        "message":f"Post With {id} deleted SuccesFully"
    }
@app.put("/UpdateDBposts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post,db:Session = Depends(get_db)):
    # Check if the post exists in the database
    existing_post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )

    for key, value in post.dict().items():
        setattr(existing_post,key,value)
    
    db.commit()
    db.refresh(existing_post)

    return {"data": existing_post}

