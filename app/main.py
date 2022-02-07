from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break;
    except Exception as error:
        print('connection failed')
        print(error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Welcome to my api 2"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, response: Response, db: Session = Depends(get_db)):
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
    return {"data": new_post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id==id)
    if not query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    query.delete(synchronize_session=False)
    db.commit() 
    
    return {'message': query}

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_posts(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s returning *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id== id)
    post_db = post_query.first()
    if post_db == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="That id does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}