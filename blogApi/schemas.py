from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class User(BaseModel):
    email : EmailStr
    
    class Config:
        orm_mode = True