from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.base import Base
from .repositories.session import engine

import firebase_admin
from firebase_admin import credentials

from .features.auth.auth_controller import router as auth_router
from .features.remote.remote_controller import router as remote_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
    "http://localhost:1420"
]


cred = credentials.Certificate("keys/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(remote_router)