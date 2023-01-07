from uuid import uuid4
from fastapi import FastAPI
from models import Gender, Role, User
from typing import List

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), first_name="Tim", middle_name="Ian",
         last_name="Atwanzire", gender=Gender.male, role=[Role.student]),
    User(id=uuid4(), first_name="Tony", middle_name="Adrian",
         last_name="Asinja", gender=Gender.male, role=[Role.user])
]


@app.get("/")
async def root():
    return {"body": "Hello World ..."}

@app.get("/v1/api/users")
async def fetch_users():
    return db

@app.post("/v1/api/users")
async def create_user(user : User):
    db.append(user)
    return {"id" : user.id}