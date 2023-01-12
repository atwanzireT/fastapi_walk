from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None

@app.get('/items/', response_model=Item)
def create_items(item:Item):
    return item

@app.post('/post/', response_model=UserIn)
def create_user(user:UserIn):
    return user