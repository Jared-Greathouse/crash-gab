from app.logging_config import setup_logging

setup_logging()

from fastapi import FastAPI
from app.api.chatroom_api import router as chatroom_router
import logging
import psutil

from app.middleware.timer import TimingMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(TimingMiddleware)

app.include_router(chatroom_router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    """Enhanced health check endpoint that includes system metrics"""
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data = {
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent
            }
        }
        
        logger.info(f"Health check completed: {health_data}")
        return health_data
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return {"status": "unhealthy", "error": str(e)}