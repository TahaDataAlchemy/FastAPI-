from fastapi import HTTPException, status, Depends, APIRouter
from app import schema,models,Oauth2,ORM
from sqlalchemy.orm import Session
router  = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db:Session = Depends(ORM.get_db),current_user:int = Depends(Oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {vote.post_id} does not Exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user["id"]) #Composite Key (Vote.post_id+current_user_id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            """" post agar vote k table me mill jati hai (agar vote = 1 or oske bad bhi post mill jati hai vote table me means vote phele se hua wa hai)
                 iska mtlb hai tu hum exception raise kardenge else add karde k vote k table me 
            """
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"{current_user["id"]} has allready voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user["id"])
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message":"successfully deleted vote"}
