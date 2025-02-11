from fastapi import HTTPException, status, Depends, APIRouter
from app import models, utils   #That model.user validate the post request before adding it into db 
from app.ORM import get_db
from sqlalchemy.orm import Session
from app.schema import UserValidation, CreatedUserResponse
from typing import List

router = APIRouter(
    prefix="/user",# Use as a prefix like (/user/Createusers)
    tags=['Users'] # Using For grouping same API on swagger UI
    
)   #Now Working with both usecase (User and Post) with routers so we only initialize fastapi once and use it in entire project 

@router.post("/Createusers", status_code=status.HTTP_201_CREATED, response_model=CreatedUserResponse)
def create_user(user: UserValidation, db: Session = Depends(get_db)):
    # Check if a user with the same email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    # Hash the password and create a new user
    hashed_password = utils.hashpass(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=CreatedUserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    # Retrieve a user by ID
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this ID does not exist",
        )
    return user

@router.get("/AllUsers",status_code=status.HTTP_200_OK,response_model=List[CreatedUserResponse])
def getAllUsers(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
