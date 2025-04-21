from app.logging_config import setup_logging

setup_logging()

import os
from fastapi import FastAPI
from app.api.chatroom_api import router as chatroom_router
# from app import logging_config  # This will initialize logging
# import logging

app = FastAPI()

app.include_router(chatroom_router)

@app.get("/")
def read_root():
    logger = logging.getLogger(__name__)
    logger.info("Root endpoint accessed")
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}