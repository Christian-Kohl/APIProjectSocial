from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my api 2"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

@app.post("/post")
def create_post(post: Post):
    print(post)
    return {"new_post": f"title {post.title} content {post.content}"}