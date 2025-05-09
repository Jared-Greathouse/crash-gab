from app.services import chatroom_service
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chatroom_models import ChatroomInDB, ChatroomUpdate
from typing import Dict
import logging
logger = logging.getLogger(__name__)

async def list_chatrooms(db: AsyncIOMotorDatabase):
    try:
        logger.debug("Listing chatrooms in controller")
        chatrooms = await chatroom_service.get_all_chatrooms(db)
        logger.info("Controller successfully fetched chatrooms")
        return chatrooms
    except ValueError as e:
        logger.warning(f"ValueError in controller: {e}")
        raise e  # Pass it up to be translated to HTTP
    except Exception as e:
        logger.error(f"Unexpected error in controller: {e}")
        raise RuntimeError("Controller failed to fetch chatrooms") from e

async def get_chatroom_by_id(db: AsyncIOMotorDatabase, chatroom_id: str):
    try:
        logger.debug(f"Fetching chatroom with ID: {chatroom_id} in controller")
        chatroom = await chatroom_service.get_chatroom_by_id(db, chatroom_id)
        logger.info(f"Controller successfully fetched chatroom with ID: {chatroom_id}")
        return chatroom
    except ValueError as e:
        logger.warning(f"ValueError in controller: {e}")
        raise e  # Pass it up to be translated to HTTP
    except Exception as e:
        logger.error(f"Unexpected error in controller: {e}")
        raise RuntimeError("Controller failed to fetch chatroom") from e

async def create_chatroom(db: AsyncIOMotorDatabase, chatroom_data: ChatroomInDB):
    try:
        logger.debug(f"Creating chatroom in controller: {chatroom_data}")
        chatroom_id = await chatroom_service.create_chatroom(db, chatroom_data)
        logger.info(f"Controller successfully created chatroom with ID: {chatroom_id}")
        return chatroom_id
    except ValueError as e:
        logger.warning(f"ValueError in controller: {e}")
        raise e  # Pass it up to be translated to HTTP
    except Exception as e:
        logger.error(f"Unexpected error in controller: {e}")
        raise RuntimeError("Controller failed to create chatroom") from e

async def update_chatroom(db: AsyncIOMotorDatabase, chatroom_id: str, chatroom_data: ChatroomUpdate):
    try:
        logger.debug(f"Updating chatroom in controller: {chatroom_id}")
        result = await chatroom_service.update_chatroom(db, chatroom_id, chatroom_data)
        logger.info(f"Controller successfully updated chatroom with ID: {chatroom_id}")
        return result
    except ValueError as e:
        logger.warning(f"ValueError in controller: {e}")
        raise e  # Pass it up to be translated to HTTP
    except Exception as e:
        logger.error(f"Unexpected error in controller: {e}")
        raise RuntimeError("Controller failed to update chatroom") from e

async def delete_chatroom(db: AsyncIOMotorDatabase, chatroom_id: str) -> Dict[str, int]:
    try:
        logger.debug(f"Deleting chatroom in controller: {chatroom_id}")
        result = await chatroom_service.delete_chatroom(db, chatroom_id)
        logger.info(f"Controller successfully deleted chatroom with ID: {chatroom_id}")
        return result
    except ValueError as e:
        logger.warning(f"ValueError in controller: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in controller: {e}")
        raise
