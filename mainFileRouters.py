from fastapi import FastAPI
from app.routers import post, userRouters,auth,votes  # Import routers
from app.ORM import engine
from app import models
from .config import settings

models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(post.router)
app.include_router(userRouters.router)
app.include_router(auth.router)
app.include_router(votes.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}
