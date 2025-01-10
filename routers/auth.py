from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema import UserValidation
import app.models
from app.ORM import  get_db
from app import utils,Oauth2
from pydantic import EmailStr,ValidationError
router = APIRouter(tags=["Authentication"])

#Oauth2password me hume apne custom name ki jaga username likhna hai or post man se input form se jae ga
@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    try:
        email = EmailStr._validate(user_credentials.username)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Email Format")
    
    user = db.query(app.models.User).filter(app.models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials"
        )
    #create Token
    access_token = Oauth2.creat_acess_token(data = {"user_id":user.email,"id":user.id}) # This token saves in cookie so when every time i logged in it will not require password untill the token expires (like watsapp web)
    #return token
    return {"acess_token":access_token,"token_type":"bearer"}