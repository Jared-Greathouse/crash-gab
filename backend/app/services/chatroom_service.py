from app.repositories import chatroom_repository
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chatroom_models import ChatroomInDB 
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

async def get_chatroom_by_id(db: AsyncIOMotorDatabase, chatroom_id: str):
    logger.debug(f"Fetching chatroom with ID: {chatroom_id} from service layer")
    try:
        chatroom = await chatroom_repository.get_chatroom_by_id(db, chatroom_id)
        if not chatroom:
            logger.warning(f"No chatroom found with ID: {chatroom_id} in service layer")
            raise ValueError("No chatroom found")
        return chatroom
    except Exception as e:
        logger.error(f"Error fetching chatroom: {e}")
        raise e

async def create_chatroom(db: AsyncIOMotorDatabase, chatroom_data: ChatroomInDB):
    logger.debug(f"Creating chatroom: {chatroom_data}")
    try:
        chatroom_id = await chatroom_repository.create_chatroom(db, chatroom_data)
        logger.info(f"Chatroom created successfully: {chatroom_id}")
        return chatroom_id
    except Exception as e:
        logger.error(f"Error creating chatroom in service layer: {e}")
        raise e

