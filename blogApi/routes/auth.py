from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from core.database import get_db
from core.schemas import UserLogin
from core import models
from core import utils

router =APIRouter(tags=["Authentication"])

@router.post("/auth")
def login(user_credentials: UserLogin, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong Credentials")

    if not utils.verify(user_credentials.password, models.User.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong Credentials")

    # create token
    # return token
    return {"token": "example token"}