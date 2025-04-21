import pytest
from unittest.mock import AsyncMock
from app.services import chatroom_service
from app.controllers import chatroom_controller
from app.models.chatroom_models import ChatroomInDB

class AsyncIterator:
    def __init__(self, items):
        self.items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.items:
            raise StopAsyncIteration
        return self.items.pop(0)

@pytest.mark.asyncio
async def test_get_all_chatrooms_success():
    mock_db = AsyncMock()
    mock_db["chatrooms"].find.return_value = AsyncIterator([
        {"_id": "1", "name": "General", "messages": [], "members": []}
    ])
    result = await chatroom_controller.list_chatrooms(mock_db)
    assert len(result) == 1
    assert result[0]["name"] == "General"

@pytest.mark.asyncio
async def test_get_all_chatrooms_empty():
    mock_db = AsyncMock()
    mock_db["chatrooms"].find.return_value = AsyncIterator([])
    with pytest.raises(ValueError, match="No chatrooms found"):
        await chatroom_controller.list_chatrooms(mock_db)

@pytest.mark.asyncio
async def test_get_all_chatrooms_db_error():
    mock_db = AsyncMock()
    mock_db["chatrooms"].find.side_effect = Exception("DB error")
    with pytest.raises(RuntimeError, match="Controller failed to fetch chatrooms"):
        await chatroom_controller.list_chatrooms(mock_db)