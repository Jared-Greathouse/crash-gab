from app.services import chatroom_service
from motor.motor_asyncio import AsyncIOMotorDatabase

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
