from app.repositories import chatroom_repository

def get_all_chatrooms():
    return chatroom_repository.get_all_chatrooms()
