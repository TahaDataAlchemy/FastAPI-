from jose import JWSError, jwt
from datetime import datetime, timedelta
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
