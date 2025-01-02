#Validating Our Model
from pydantic import BaseModel
from typing import Optional

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

class ApiResponsetoUser(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None
