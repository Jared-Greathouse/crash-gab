import os
from fastapi import FastAPI
from app.api.chatroom_api import router as chatroom_router

app = FastAPI()

app.include_router(chatroom_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}