from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import HTTPException,status
import psycopg2
from psycopg2.extras import RealDictCursor # use for geting postgres column 
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:int

while True:
    try:
        conn = psycopg2.connect(host = "localhost",database = "fastapi",user ="postgres",password = 'admin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database SuccessFully Connected")
        break
    except Exception as error:
        print("Connecting To Database Failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/DBposts",status_code=status.HTTP_200_OK)
def get_Db_Post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/creatingPost",status_code=status.HTTP_201_CREATED)
def PostCreated(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published,rating) VALUES (%s,%s,%s,%s) RETURNING *""",
                    (post.title,post.content,post.published,post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}


def find_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""",(id,))
    postbyid = cursor.fetchone()
    return postbyid

@app.get("/DBposts/{id}",status_code=status.HTTP_200_OK)
def getSinglePost(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} is not Found"
        )
    return {"data":post}

@app.delete("/DBposts/{id}",status_code=status.HTTP_200_OK)
def deletingSimplePostFromDB(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post With ID {id} does not Exist"
        )
    return {
        "message":f"Post With {id} deleted SuccesFully"
    }
@app.put("/UpdateDBposts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    # Check if the post exists in the database
    existing_post = find_post(id)
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )

    # Update the post in the database
    cursor.execute(
        """UPDATE posts 
           SET title = %s, content = %s, published = %s 
           WHERE id = %s 
           RETURNING *""",
        (post.title, post.content, post.published, id)
    )

    updated_post = cursor.fetchone()  # Fetch the updated post
    conn.commit()  # Commit the transaction

    # Return the updated post as the response
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update the post with ID {id}"
        )

    return {"data": updated_post}

