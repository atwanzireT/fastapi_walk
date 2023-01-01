from fastapi import FastAPI, status, Response, HTTPException, Depends
from . import database
from pydantic import BaseModel
from . import models
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
import time

models.Base.metadata.create_all(engine)

app = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


# @app.get('/posts')
# def get_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {'data': posts}

@app.get('/posts')
def get_post(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    
@app.get('/sqlalchemy')
def test_posts(db : Session = Depends(get_db)):
    return {"status":"success"}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createpost(post: Post, db : Session = Depends(get_db)):
    new_post = models.Post(title = post.title, content = post.content, published = post.is_published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def createpost(post: Post):
#     cursor.execute("""INSERT INTO posts(title, content, is_published) values (%s, %s, %s) RETURNING *
#     """, (post.title, post.content, post.is_published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchall()
    return {"Post Detail": post}


def find_post_index():
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchall()
    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


# @app.update("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_post_index(id)

#     if index == None:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     post_dict = post.dict()
#     post['id'] = id
#     my_posts[index] = post_dict
#     return {'message': post_dict}
