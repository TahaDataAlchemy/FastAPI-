from fastapi import HTTPException,status,Depends,APIRouter
from ..models import Post as PostModelDB
from typing import List
from ..ORM import engine,get_db
from sqlalchemy.orm import Session
from ..schema import UpdatingPost,CreatePost,ApiResponsetoUser


router = APIRouter(
    prefix="/post",
    tags=["Posts"]  # Using For grouping same API on swagger UI
    
)#Now Working both usecase with routers so we only initialize fastapi once and use it in entire project 


#Use to retrieve All Post present in Memory
@router.get("/DBposts",status_code=status.HTTP_200_OK,response_model=List[ApiResponsetoUser])
def get_Db_Post(db: Session = Depends(get_db)):
    posts = db.query(PostModelDB).all()
    return posts

@router.post("/creatingPost",status_code=status.HTTP_201_CREATED,response_model=ApiResponsetoUser)
def PostCreated(post:CreatePost,db:Session = Depends(get_db)):
    new_post = PostModelDB(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #Refresh to get generated Fields
    return new_post

@router.get("/DBposts/{id}",status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
def getSinglePost(id: int,db:Session = Depends(get_db)):
    post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} is not Found"
        )
    return post

@router.delete("/DBposts/{id}",status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
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
@router.put("/UpdateDBposts/{id}", status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
def update_post(id: int, post: UpdatingPost,db:Session = Depends(get_db)):
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

    return existing_post

