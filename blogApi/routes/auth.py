from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from core.database import get_db
from core.schemas import UserLogin
from core import models, utils, Oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/auth")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create token
    access_token = Oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"token": access_token, "token_type":"bearer"}
