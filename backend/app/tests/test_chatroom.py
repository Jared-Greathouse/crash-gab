import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services import chatroom_service
from app.controllers import chatroom_controller
from app.models.chatroom_models import ChatroomInDB
from bson.objectid import ObjectId
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

@pytest.mark.asyncio
async def test_get_chatroom_by_id_success():
    # Create the base mock
    mock_db = MagicMock()
    # Create an AsyncMock for find_one
    mock_find_one = AsyncMock()
   # Use a valid ObjectId string (24 hex characters)
    valid_id = "507f1f77bcf86cd799439011"
    mock_find_one.return_value = {
        "_id": ObjectId(valid_id),
        "name": "Tech",
        "messages": [],
        "members": []
    }
    # Set up the dictionary-style access to return a mock with the async find_one
    mock_collection = MagicMock()
    mock_collection.find_one = mock_find_one
    mock_db.__getitem__.return_value = mock_collection
    
    result = await chatroom_controller.get_chatroom_by_id(mock_db, valid_id)
    assert result["name"] == "Tech"
    mock_find_one.assert_called_once_with({"_id": ObjectId(valid_id)})

@pytest.mark.asyncio
async def test_get_chatroom_by_id_not_found():
    # Create the base mock
    mock_db = MagicMock()
    # Create an AsyncMock for find_one
    mock_find_one = AsyncMock()
    mock_find_one.return_value = None
    # Set up the dictionary-style access to return a mock with the async find_one
    mock_collection = MagicMock()
    mock_collection.find_one = mock_find_one
    mock_db.__getitem__.return_value = mock_collection
    
    # Use a valid ObjectId string that doesn't exist in the DB
    valid_nonexistent_id = ObjectId("507f1f77bcf86cd799439012")

    with pytest.raises(ValueError, match="No chatroom found"):
        await chatroom_controller.get_chatroom_by_id(mock_db, valid_nonexistent_id)
    mock_find_one.assert_called_once_with({"_id": valid_nonexistent_id})

@pytest.mark.asyncio
async def test_get_chatroom_by_id_invalid_id():
    # Create the base mock
    mock_db = MagicMock()
    # Test with an invalid ObjectId
    invalid_id = "invalid_id"
    with pytest.raises(ValueError, match="Invalid ObjectId format"):
        await chatroom_controller.get_chatroom_by_id(mock_db, invalid_id)
