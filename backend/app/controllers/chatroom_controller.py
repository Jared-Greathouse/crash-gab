from app.services import chatroom_service
from motor.motor_asyncio import AsyncIOMotorDatabase

async def list_chatrooms(db: AsyncIOMotorDatabase):
    try:
        return await chatroom_service.get_all_chatrooms(db)
    except ValueError as e:
        raise e  # Pass it up to be translated to HTTP
    except Exception as e:
        raise RuntimeError("Controller failed to fetch chatrooms") from e
