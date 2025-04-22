from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, UTC
from bson import ObjectId

class User(BaseModel):
    username: str

class Message(BaseModel):
    content: str
    sender: User

class Chatroom(BaseModel):
    name: str
    messages: Optional[list[Message]]
    members: Optional[list[User]]


class ChatroomInDB(Chatroom):
    _id: ObjectId
    active: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
