#Validating Our Model
from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime

from pydantic.types import conint #use for specifying vote 0 AND 1 specifically , cons = it allowed negative number so handle it accordingly 
class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None #its optional if not a value no problem None will return

#Making More Schema Validation , like if i am CreatingPost i need a CreatePost Validation, and if i am updating I need a seperate Function for it 

class CreatePost(PostBase):
    pass
class UpdatingPost(PostBase):
    published:bool # In Updating Post we are telling User to set published explicitly not a default value,This is where why i need more than one schema validations


class UserValidation(BaseModel):
    email:EmailStr
    password:str

class CreatedUserResponse(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime

class ApiResponsetoUser(BaseModel):
    id:int
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None
    owner:CreatedUserResponse

class VoteResponse(BaseModel):
    Post:ApiResponsetoUser
    LikeCount: int

class LoginValidation(BaseModel):
    email: EmailStr
    password:str

class TokenResponse(BaseModel):
    acess_token :str
    token_type : str

class TokenData(BaseModel):
    id: int
    email:EmailStr

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1) 