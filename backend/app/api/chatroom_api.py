from fastapi import APIRouter, Depends
from app.controllers import chatroom_controller
from app.database.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/chatrooms", tags=["Chatrooms"])

@router.get("/")
async def list_all(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await chatroom_controller.list_chatrooms(db)
