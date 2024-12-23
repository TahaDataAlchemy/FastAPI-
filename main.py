from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None #its optional if not a value no problem None will return

#Making a simple data to deal it with 
my_posts = [{"title":"title of post 1","content":"Content of Post 1","id":1},{
            "title":"title of post 2","content":"Content of Post 2","id":2
}]
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/Dataposts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts")
def create_post(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000000000000)
    my_posts.append(post_dict)
    return {"data":post_dict}






# @app.post("/posts")
# def create_post(post: Post):
#     print(post) # this will print in the way of Pydantict
#     print(post.dict()) #this will print int the way of dict
#     return{"data":"new_post"}


# #A way to retrieve data from the postman 
# @app.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return  {"new_post":f"{payload["title"] , payload["content"]}"}