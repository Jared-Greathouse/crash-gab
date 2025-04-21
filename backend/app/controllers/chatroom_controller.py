from app.services import chatroom_service
from motor.motor_asyncio import AsyncIOMotorDatabase

async def list_chatrooms(db: AsyncIOMotorDatabase):
    return await chatroom_service.get_all_chatrooms(db)
