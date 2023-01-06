from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, utils
from ..schemas import Post, PostBase, CreatePost
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = "/posts"
)

@router.get('/', response_model=List[Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def createpost(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).all()
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, post:PostBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} doesn't exist ...")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",  status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
