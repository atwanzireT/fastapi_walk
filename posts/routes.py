from fastapi import FastAPI, status
from . import database
from pydantic import BaseModel
from .database import cursor

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    is_published : bool = True
    
@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}

@app.post('/posts', status_code= status.HTTP_201_CREATED)
def createpost(post:Post):
    cursor.execute("""INSERT INTO posts(title, content, is_published) values (%s, %s, %s) RETURNING *
    """, (post.title, post.content, post.is_published))
    new_post = cursor.fetchone()
    return {"data":new_post}