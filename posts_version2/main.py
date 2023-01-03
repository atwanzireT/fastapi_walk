from fastapi import FastAPI, status, Response, HTTPException, Depends
from . import database
from . import models
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
import time
from .schemas import *
from typing import List
from passlib.context import CryptContext

models.Base.metadata.create_all(engine)

app = FastAPI()
pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated = "auto")
# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/posts')
# def get_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {'data': posts}

@app.get('/posts', response_model=List[Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def createpost(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).all()
    return  post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, post:PostBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} doesn't exist ...")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/{id}",  status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# User
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = pwd_crypt.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# def find_post_index():
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     delete_post = cursor.fetchall()
#     conn.commit()
#     return Response(status_code = status.HTTP_204_NO_CONTENT)


# @app.update("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_post_index(id)

#     if index == None:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     post_dict = post.dict()
#     post['id'] = id
#     my_posts[index] = post_dict
#     return {'message': post_dict}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def createpost(post: Post):
#     cursor.execute("""INSERT INTO posts(title, content, is_published) values (%s, %s, %s) RETURNING *
#     """, (post.title, post.content, post.is_published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


# @app.get("/posts/{id}")
# def get_post(id: str):
#     cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchall()
#     return {"Post Detail": post}
