from fastapi import HTTPException,status,Depends,APIRouter
from ..models import Post as PostModelDB
from ..models import Vote as VoteTable
from typing import List
from ..ORM import engine,get_db
from sqlalchemy.orm import Session
from ..schema import UpdatingPost,CreatePost,ApiResponsetoUser,VoteResponse
from typing import Optional
from app import Oauth2
from sqlalchemy.orm import aliased
from sqlalchemy import func

router = APIRouter(
    prefix="/post", # Use as a prefix like (/post/DBposts)
    tags=["Posts"]  # Using For grouping same API on swagger UI
    
)#Now Working both usecase with routers so we only initialize fastapi once and use it in entire project 

#Use to retrieve All Post present in Memory
@router.get("/DBposts",status_code=status.HTTP_200_OK,response_model=List[VoteResponse])
def get_Db_Post(db: Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user),limit:int = 10,skip: int = 0,search: Optional[str] = ""): #by default limit of the result (QuerryParameter) = 10 , after question mark in URL all are querry parameter
    # posts = db.query(PostModelDB).all()
    """ 
        Note User_data in the funxtion Prameter contain id and email from login Table
        limit, skip and search is the query parameter
        PostModelDb is taking ownner id from db(Post_Table) and User_data is taking id from users table and after matching them it send only those post which matched both ids
        search paremeter remains optional mean we dont need to provide the search content untill it is required
        post/DBposts?limit=2&skip=1&search=BST%20Graphs = this querry parameter (%20 is used for space)
    """

    posts = (
    db.query(PostModelDB)
    .filter(PostModelDB.ownner_id == user_data["id"]) #filtering on the basis of owner id
    .filter(PostModelDB.content.contains(search)) #filter on the basis of content
    .limit(limit) #limiting on the basis of querry parameter
    .offset(skip) #skipping on the basis of querry parameter
    .all()
    )
    
    result = (
    db.query(
        PostModelDB,
        func.count(VoteTable.user_id).label("LikeCount"),
    )
    .outerjoin(VoteTable, PostModelDB.id == VoteTable.post_id)
    .filter(PostModelDB.ownner_id == user_data["id"])  # ✅ Filter by logged-in user
    .filter(PostModelDB.content.contains(search))  # ✅ Search filter
    .group_by(PostModelDB.id, PostModelDB.ownner_id, PostModelDB.title, PostModelDB.content)  # ✅ Moved before limit/offset
    .order_by(func.count(VoteTable.user_id).desc())  # ✅ Order by votes
    .limit(limit)  # ✅ Limit
    .offset(skip)  # ✅ Offset
    .all()
    )

    return result

@router.post("/creatingPost",status_code=status.HTTP_201_CREATED,response_model=ApiResponsetoUser)
def PostCreated(post:CreatePost,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    print(user_data)
    new_post = PostModelDB(ownner_id =user_data['id'],**post.dict()) # Assigining Ownner_id (FK) in post table from with user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #Refresh to get generated Fields
    return new_post

@router.get("/DBposts/{id}",status_code=status.HTTP_200_OK,response_model=VoteResponse)
def getSinglePost(id: int,db:Session = Depends(get_db),user_data:dict  = Depends(Oauth2.get_current_user)):
    # post = db.query(PostModelDB).filter(PostModelDB.id == id).first()

    post = (
        db.query(
            PostModelDB,
            func.count(VoteTable.user_id).label("LikeCount"),
        )
        .outerjoin(VoteTable, PostModelDB.id == VoteTable.post_id)
        .filter(PostModelDB.ownner_id == user_data["id"])  # ✅ Filter by logged-in user
        .filter(PostModelDB.id == id)  # ✅ Ensure we fetch a specific post ID
        .group_by(PostModelDB.id, PostModelDB.ownner_id, PostModelDB.title, PostModelDB.content)  # ✅ Group by necessary fields
        .order_by(func.count(VoteTable.user_id).desc())  # ✅ Order by LikeCount
        .first()
    )
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

