from fastapi import HTTPException,status,Depends,APIRouter
from ..models import Post as PostModelDB
from typing import List
from ..ORM import engine,get_db
from sqlalchemy.orm import Session
from ..schema import UpdatingPost,CreatePost,ApiResponsetoUser
from app import Oauth2

router = APIRouter(
    prefix="/post", # Use as a prefix like (/post/DBposts)
    tags=["Posts"]  # Using For grouping same API on swagger UI
    
)#Now Working both usecase with routers so we only initialize fastapi once and use it in entire project 

#Note User_data in the funxtion Prameter contain id and email from login Table
#Use to retrieve All Post present in Memory
@router.get("/DBposts",status_code=status.HTTP_200_OK,response_model=List[ApiResponsetoUser])
def get_Db_Post(db: Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    # posts = db.query(PostModelDB).all()
    posts = db.query(PostModelDB).filter(PostModelDB.ownner_id == user_data["id"]).all() #PostModelDb is taking ownner id from db(Post_Table) and User_data is taking id from users table and after matching them it send only those post which matched both ids
    return posts

@router.post("/creatingPost",status_code=status.HTTP_201_CREATED,response_model=ApiResponsetoUser)
def PostCreated(post:CreatePost,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    print(user_data)
    new_post = PostModelDB(ownner_id =user_data['id'],**post.dict()) # Assigining Ownner_id (FK) in post table from with user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #Refresh to get generated Fields
    return new_post

@router.get("/DBposts/{id}",status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
def getSinglePost(id: int,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} is not Found"
        )
    if post.id!=user_data["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail = "Not Allowed to perfrom this operation"
        )
    return post

@router.delete("/DBposts/{id}",status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
def deletingSimplePostFromDB(id: int,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    deleted_post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post With ID {id} does not Exist"
        )
    if deleted_post.ownner_id!=user_data["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail = "Not Authorized to perfrom this requested action"
        )
    db.delete(deleted_post)
    db.commit()
    return {
        "title": "Post Deleted",
        "content": f"Post With ID {id} was successfully deleted.",
        "published": True,
        "rating": None,  # Optional field; you can also omit this field
    }
@router.put("/UpdateDBposts/{id}", status_code=status.HTTP_200_OK,response_model=ApiResponsetoUser)
def update_post(id: int, post: UpdatingPost,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    # Check if the post exists in the database
    existing_post = db.query(PostModelDB).filter(PostModelDB.id == id).first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
    if existing_post.ownner_id!=user_data["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail = "Not Authorized to perfrom this requested action"
        )

    for key, value in post.dict().items():
        setattr(existing_post,key,value)
    
    db.commit()
    db.refresh(existing_post)

    return existing_post

