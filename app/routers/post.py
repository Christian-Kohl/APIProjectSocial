from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # cursor.execute("""INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                   (post.title,
    #                   post.content,
    #                   post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id==id)
    if not query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    query.delete(synchronize_session=False)
    db.commit() 
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s returning *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id== id)
    post_db = post_query.first()
    if post_db == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="That id does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()