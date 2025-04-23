import pytest
from unittest.mock import AsyncMock, MagicMock, create_autospec
from app.services import chatroom_service
from app.controllers import chatroom_controller
from app.models.chatroom_models import ChatroomInDB, ChatroomUpdate
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
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


@pytest.mark.asyncio
async def test_create_chatroom_success():
    # Create the base mock
    mock_db = MagicMock()
    
    # Create an AsyncMock for insert_one
    mock_insert_one = AsyncMock()
    inserted_id = ObjectId("507f1f77bcf86cd799439011")
    mock_insert_one.return_value = AsyncMock(inserted_id=inserted_id)
    
    # Set up the dictionary-style access to return a mock with the async insert_one
    mock_collection = MagicMock()
    mock_collection.insert_one = mock_insert_one
    mock_db.__getitem__.return_value = mock_collection
    
    # Create test data
    chatroom_data = ChatroomInDB(
        name="New Chatroom",
        messages=[],
        members=[],
        _id=inserted_id,  # Required by the model
        active=True
    )
    
    result = await chatroom_controller.create_chatroom(mock_db, chatroom_data)
    
    # Verify the result
    assert isinstance(result, dict)
    assert result["_id"] == str(inserted_id)
    
    # Verify insert_one was called with the correct data
    mock_insert_one.assert_called_once()
    call_args = mock_insert_one.call_args[0][0]
    assert call_args["name"] == "New Chatroom"
    assert call_args["messages"] == []
    assert call_args["members"] == []
    assert call_args["active"] is True
    assert "_id" not in call_args

@pytest.mark.asyncio
async def test_create_chatroom_db_error():
    mock_db = AsyncMock()
    chatroom_data = ChatroomInDB(name="FailRoom", messages=[], members=[])
    mock_db["chatrooms"].insert_one.side_effect = Exception("Insert failed")

    with pytest.raises(RuntimeError, match="Controller failed to create chatroom"):
        await chatroom_controller.create_chatroom(mock_db, chatroom_data)

@pytest.mark.asyncio
async def test_update_chatroom_db_error():
    mock_db = MagicMock()
    mock_db["chatrooms"].find_one.return_value = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "name": "Tech",
        "messages": [],
        "members": [],
        "active": True
    }
    mock_db["chatrooms"].update_one.side_effect = Exception("Update failed")
    with pytest.raises(RuntimeError, match="Controller failed to update chatroom"):
        await chatroom_controller.update_chatroom(mock_db, "507f1f77bcf86cd799439011", {
            "name": "Updated Tech"
        })


@pytest.mark.asyncio
async def test_update_chatroom_success():
    # Create the base mock
    mock_db = MagicMock()
    
    # Create an AsyncMock for update_one that returns a real UpdateResult
    mock_update_one = AsyncMock()
    # Create a real UpdateResult object
    update_result = UpdateResult({
        'n': 1,
        'nModified': 1,
        'ok': 1.0,
        'updatedExisting': True
    }, acknowledged=True)
    mock_update_one.return_value = update_result
    
    # Set up the dictionary-style access to return a mock with the async update_one
    mock_collection = MagicMock()
    mock_collection.update_one = mock_update_one
    mock_db.__getitem__.return_value = mock_collection
    
    # Create update data using the Pydantic model
    update_data = ChatroomUpdate(name="Updated Tech")
    chatroom_id = "507f1f77bcf86cd799439011"
    
    result = await chatroom_controller.update_chatroom(mock_db, chatroom_id, update_data)
    
    # Verify the result
    assert isinstance(result, dict)
    assert result["matched_count"] == 1
    assert result["modified_count"] == 1
    
    # Verify update_one was called with correct arguments
    mock_update_one.assert_called_once_with(
        {"_id": ObjectId(chatroom_id)},
        {"$set": update_data.model_dump(exclude_unset=True)}
    )

@pytest.mark.asyncio
async def test_update_chatroom_not_found():
    # Create the base mock
    mock_db = MagicMock()
    
    # Create an AsyncMock for update_one that returns a real UpdateResult
    mock_update_one = AsyncMock()
    # Create a real UpdateResult object for not found case
    update_result = UpdateResult({
        'n': 0,
        'nModified': 0,
        'ok': 1.0,
        'updatedExisting': False
    }, acknowledged=True)
    mock_update_one.return_value = update_result
    
    # Set up the dictionary-style access to return a mock with the async update_one
    mock_collection = MagicMock()
    mock_collection.update_one = mock_update_one
    mock_db.__getitem__.return_value = mock_collection
    
    # Create update data using the Pydantic model
    update_data = ChatroomUpdate(name="Updated Tech")
    chatroom_id = "507f1f77bcf86cd799439011"
    
    with pytest.raises(ValueError, match="No chatroom found"):
        await chatroom_controller.update_chatroom(mock_db, chatroom_id, update_data)
    
    # Verify update_one was called with correct arguments
    mock_update_one.assert_called_once_with(
        {"_id": ObjectId(chatroom_id)},
        {"$set": update_data.model_dump(exclude_unset=True)}
    )