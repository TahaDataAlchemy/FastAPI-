from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from app.schema import UserValidation
import app.models
from app.ORM import  get_db
from app import utils
router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_credentials:UserValidation,db:Session = Depends(get_db)):
    user = db.query(app.models.User).filter(app.models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials"
        )
    #create Token
    #return token
    return {"token":"example token"}