from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, utils
from .schemas import UserCreate, User
from .database import get_db


router = APIRouter()

# User
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user{id}", status_code=status.HTTP_200_OK)
def get_user(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).all()
    return user