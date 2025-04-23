from fastapi import APIRouter, Depends, HTTPException
from app.controllers import chatroom_controller
from app.database.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.chatroom_models import ChatroomInDB, ChatroomUpdate
router = APIRouter(prefix="/chatrooms", tags=["Chatrooms"])

@router.get("/")
async def list_all(db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        return await chatroom_controller.list_chatrooms(db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{chatroom_id}")
async def get_chatroom(chatroom_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        return await chatroom_controller.get_chatroom_by_id(db, chatroom_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", status_code=201)
async def create_chatroom(chatroom_data: ChatroomInDB, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        chatroom_id = await chatroom_controller.create_chatroom(db, chatroom_data)
        return {"chatroom_id": chatroom_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/{chatroom_id}", status_code=200)
async def update_chatroom(chatroom_id: str, chatroom_data: ChatroomUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        modified_count = await chatroom_controller.update_chatroom(db, chatroom_id, chatroom_data)
        return {"modified_count": modified_count}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/{chatroom_id}", status_code=200)
async def delete_chatroom(chatroom_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        deleted_count = await chatroom_controller.delete_chatroom(db, chatroom_id)
        return {"deleted_count": deleted_count}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")