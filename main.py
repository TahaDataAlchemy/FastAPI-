from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import HTTPException


app = FastAPI()

#Validating Our Model
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

#Use to retrieve All Post present in Memory
@app.get("/Dataposts")
def get_posts():
    return {"data":my_posts}

#Creating A post and saving it to memory by assigning Random id and Validating from Post Class
@app.post("/posts")
def create_post(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000000000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

#Find Post By id
def findpost(id:int):
    for post in my_posts:
        if post["id"] == id:  # Access the "id" key in the dictionary
            return {"post_details": post}

    # Raise a 404 error if no post is found with the given id
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")


#Getting the singal post
@app.get("/posts/{id}")# always use int when pasing id as fastapi treat number in url as str
def get_post(id:int): 
    post = findpost(id)

    return {"postdetail":post}
    





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