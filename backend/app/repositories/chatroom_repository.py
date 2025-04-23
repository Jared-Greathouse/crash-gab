from bson.objectid import ObjectId, InvalidId
# from app.database.mongodb import db
from app.models.chatroom_models import ChatroomInDB, ChatroomUpdate
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

async def create_chatroom(db: AsyncIOMotorDatabase, chatroom_data: ChatroomInDB):
    try:
        logger.debug(f"Attempting to create chatroom: {chatroom_data}")
        # Convert the model to a dict for insertion
        chatroom_dict = chatroom_data.model_dump()
        result = await db["chatrooms"].insert_one(chatroom_dict)
        # Create the response document with the inserted ID
        created_chatroom = {
            **chatroom_dict,
            "_id": result.inserted_id
        }
        logger.debug(f"Chatroom created with ID: {result.inserted_id}")
        return serialize_chatroom(created_chatroom)
    except Exception as e:
        logger.error(f"DB error during Chatroom creation: {e}")
        raise RuntimeError("Database error") from e

async def update_chatroom(db: AsyncIOMotorDatabase, chatroom_id: str, chatroom_data: ChatroomUpdate):
    try:
        logger.debug(f"Attempting to update chatroom with ID: {chatroom_id}")
        object_id = ObjectId(chatroom_id)
        result = await db["chatrooms"].update_one(
            {"_id": object_id}, 
            {"$set": chatroom_data.model_dump(exclude_unset=True)}
        )
        if result.modified_count == 0:
            logger.warning(f"No chatroom found with ID: {chatroom_id}")
            raise ValueError(f"No chatroom found")
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    except ValueError as e:
        raise e
    except Exception as e:
        logger.error(f"DB error during Chatroom update: {e}")
        raise RuntimeError("Database error") from e
