from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, userRouters,auth,votes  # Import routers
from app.ORM import engine
from app import models
from .config import settings

# models.Base.metadata.create_all(bind=engine) no need of it now as alemboc handle migrations and creations of DB

# Initialize FastAPI app
app = FastAPI()

origins = ["*"] #can also give specific websites to access my api's specifically (*) means any website can access my apis

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #can also allow method . like if my website is just for geting data i only provide get method to perform no post
    allow_headers=["*"],
)
# Include routers
app.include_router(post.router)
app.include_router(userRouters.router)
app.include_router(auth.router)
app.include_router(votes.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}
