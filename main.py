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

my_posts = {1: {'title': 'title of post one', 'content': 'content of post one', 'id': 1}, 2: {'title': "favorite foods", "content": 'so many foods', 'id': 2}}

def find_post(id):
    return my_posts[id]

@app.get("/")
def root():
    return {"message": "Welcome to my api 2"}

@app.get("/posts")
def get_posts():
    return {'data': my_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    return {"post_detail": post}

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_id = len(my_posts) + 1
    post_dict['id'] = post_id
    my_posts[post_id] = post_dict
    return {"data": post_dict}