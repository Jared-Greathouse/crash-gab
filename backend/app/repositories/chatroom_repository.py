
# from app.database.mongodb import db
from app.models.chatroom_models import ChatroomInDB
from motor.motor_asyncio import AsyncIOMotorDatabase

# collection = db["chatrooms"]

async def get_all_chatrooms(db: AsyncIOMotorDatabase):
    return [room async for room in db["chatrooms"].find()]

# chatrooms = [
#     {"id": 1, "name": "General", "description": "Talk about anything"},
#     {"id": 2, "name": "Tech", "description": "Discuss tech topics"}
# ]

# def get_all_chatrooms():
#     return chatrooms
