from app.repositories import chatroom_repository
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
logger = logging.getLogger(__name__)

async def get_all_chatrooms(db: AsyncIOMotorDatabase):
    logger.debug("Fetching chatrooms from service layer")
    try:
        chatrooms = await chatroom_repository.get_all_chatrooms(db)
        if not chatrooms:
            logger.warning("No chatrooms found in service layer")
            raise ValueError("No chatrooms found")
        return chatrooms
    except Exception as e:
        logger.error(f"Error fetching chatrooms: {e}")
        raise e
