from app.repositories import chatroom_repository
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chatroom_models import ChatroomInDB, ChatroomUpdate
from typing import Dict
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

async def update_chatroom(db: AsyncIOMotorDatabase, chatroom_id: str, chatroom_data: ChatroomUpdate):
    logger.debug(f"Updating chatroom with ID: {chatroom_id}")
    try:
        result = await chatroom_repository.update_chatroom(db, chatroom_id, chatroom_data)
        if result["matched_count"] == 0:
            logger.warning(f"No chatroom found with ID: {chatroom_id} in service layer")
            raise ValueError("No chatroom found")
        if result["modified_count"] == 0:
            logger.warning(f"No changes made to chatroom with ID: {chatroom_id} in service layer")
            raise ValueError("No changes made")
        return result
    except Exception as e:
        logger.error(f"Error updating chatroom in service layer: {e}")
        raise e
    
async def delete_chatroom(db: AsyncIOMotorDatabase, chatroom_id: str) -> Dict[str, int]:
    logger.debug(f"Deleting chatroom with ID: {chatroom_id}")
    try:
        result = await chatroom_repository.delete_chatroom(db, chatroom_id)
        if result.get("deleted_count", 0) == 0:
            logger.warning(f"No chatroom found with ID: {chatroom_id} in service layer")
            raise ValueError("No chatroom found")
        return result
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error deleting chatroom in service layer: {e}")
        raise RuntimeError("Service error while deleting chatroom") from e