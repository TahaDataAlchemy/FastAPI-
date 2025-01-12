from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schema import Token,TokenData
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = O
#SECRET_KEY
#Algorithm
#ExpirationTimetoken

SECRET_KEY = "a5d2f3gh4567ijklmno89pqrs0tuvwxyzABCDEF"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def creat_acess_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_acess_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email: str = payload.get("user_id")
        id: str = payload.get("id")
        if id and email is None:
            raise credentials_exception
        token_data = TokenData(id = id,email=email)
    except JWTError:
        raise credentials_exception

#ye kare ga ye k token lega automatically verify kare ga verifyacesstoken se and usme se id pass nikale ga and keep me login rakhe ga 
def get_current_user(token:str = Depends()):
    pass