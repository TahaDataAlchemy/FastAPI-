from fastapi import FastAPI
from app.routers import post, userRouters  # Import routers
from app.ORM import engine
from app import models

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(post.router)
app.include_router(userRouters.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
