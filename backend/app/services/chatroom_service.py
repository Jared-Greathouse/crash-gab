from app.repositories import chatroom_repository
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_all_chatrooms(db: AsyncIOMotorDatabase):
    chatrooms = await chatroom_repository.get_all_chatrooms(db)
    if not chatrooms:
        raise ValueError("No chatrooms found")
    return chatrooms
