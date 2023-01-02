from fastapi import FastAPI, status, Response, HTTPException
from . import database
from pydantic import BaseModel
from .database import cursor, conn

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, is_published) values (%s, %s, %s) RETURNING *
    """, (post.title, post.content, post.is_published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


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
