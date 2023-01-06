from fastapi import FastAPI, status, Response, HTTPException, Depends
from .database import engine
from sqlalchemy.orm import Session
from .schemas import *
from .routers import post, user
from .database import get_db
from . import models

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

app.include_router(post.router)
app.include_router(user.router)

# @app.get('/posts')
# def get_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {'data': posts}

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
