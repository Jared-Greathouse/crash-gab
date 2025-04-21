from fastapi import APIRouter, Depends, HTTPException
from app.controllers import chatroom_controller
from app.database.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/chatrooms", tags=["Chatrooms"])

@router.get("/")
async def list_all(db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        return await chatroom_controller.list_chatrooms(db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")
