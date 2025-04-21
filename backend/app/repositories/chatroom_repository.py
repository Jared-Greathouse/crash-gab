
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


