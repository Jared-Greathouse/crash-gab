from bson.objectid import ObjectId, InvalidId
# from app.database.mongodb import db
from app.models.chatroom_models import ChatroomInDB
from motor.motor_asyncio import AsyncIOMotorDatabase

import logging
logger = logging.getLogger(__name__)

def serialize_chatroom(chatroom: dict) -> dict:
    chatroom["_id"] = str(chatroom["_id"])
    return chatroom

async def get_all_chatrooms(db: AsyncIOMotorDatabase):
    try:
        logger.debug("Attempting to fetch chatrooms from DB")
        return [serialize_chatroom(room) async for room in db["chatrooms"].find()]
    except Exception as e:
        logger.error(f"DB error: {e}")
        raise RuntimeError("Database error") from e


async def get_chatroom_by_id(db: AsyncIOMotorDatabase, chatroom_id: str):
    try:
        logger.debug(f"Attempting to fetch chatroom with ID: {chatroom_id}")
        try:
            object_id = ObjectId(chatroom_id)
        except (InvalidId, TypeError) as e:
            logger.warning(f"Invalid ObjectId format: {chatroom_id}")
            raise ValueError(f"Invalid ObjectId format: {chatroom_id}") from e
        chatroom = await db["chatrooms"].find_one({"_id": object_id})
        if chatroom:
            return serialize_chatroom(chatroom)
        else:
            logger.warning(f"No chatroom found with ID: {chatroom_id}")
            return None
    except (ValueError):
        raise
    except Exception as e:
        logger.error(f"DB error: {e}")
        raise RuntimeError("Database error") from e
