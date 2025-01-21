#This all is used for protected route like login
#Hoga ye jab bhi hum app me login karenge tu ek JWT ae ga jo k state less hoga browser me store hoga jab bhi app ko reopen karenge wo again JWT ko check karne k liye code par bheje ga. srf jwt isliye match nhi kara sakte q k JWT kahi store nhi hote server par they are stateless
#every time Jab bhi open karunga ye file JWT ko verify kare ga k galat token tu enter nhi horaha 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schema import TokenData
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.ORM import get_db
from sqlalchemy.orm import Session
from app import models
from .config import settings
#this will help me to extract the token from Autherization Header Having Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY
#Algorithm
#ExpirationTimetoken

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes

def creat_acess_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt
#the token in this parameter is comming from get_curreent_user with token extracted by header 
def verify_acess_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) # Algo in bracket because they can be in list more then one 
        email: str = payload.get("user_id")
        id: str = payload.get("id")
        if id and email is None:
            raise credentials_exception
        token_data = TokenData(id = id,email=email)
    except JWTError:
        raise credentials_exception
    
    return token_data

#ye kare ga ye k token lega automatically verify kare ga verifyacesstoken se and usme se id pass nikale ga and keep me login rakhe ga or DB ko access kare ga taqe data fetch kar sake
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):#this extract the JWT from Authentication(Bearer) Header
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers = {"WWW-Authenticate":"Bearer"}
        )
    token_data = verify_acess_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return {"id":user.id,"email":user.email}
    
