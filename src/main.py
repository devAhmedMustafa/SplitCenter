from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.base import Base
from repositories.session import engine

from features.auth.auth_controller import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)