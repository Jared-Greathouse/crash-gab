from fastapi import APIRouter
from app.controllers import chatroom_controller

router = APIRouter(prefix="/chatrooms", tags=["Chatrooms"])

@router.get("/")
def list_all():
    return chatroom_controller.list_chatrooms()
