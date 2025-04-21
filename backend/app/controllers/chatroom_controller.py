from app.services import chatroom_service

def list_chatrooms():
    return chatroom_service.get_all_chatrooms()
