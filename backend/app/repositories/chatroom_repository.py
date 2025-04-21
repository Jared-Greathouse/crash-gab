
# from app.database.mongodb import db
from app.models.chatroom_models import ChatroomInDB
from motor.motor_asyncio import AsyncIOMotorDatabase

def serialize_chatroom(chatroom: dict) -> dict:
    chatroom["_id"] = str(chatroom["_id"])
    return chatroom

async def get_all_chatrooms(db: AsyncIOMotorDatabase):
    try:
        return [serialize_chatroom(room) async for room in db["chatrooms"].find()]
    except Exception as e:
        raise RuntimeError("Database error") from e


