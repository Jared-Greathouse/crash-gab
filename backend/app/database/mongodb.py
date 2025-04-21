from motor.motor_asyncio import AsyncIOMotorClient
import os
# from fastapi import Depends

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DATABASE_NAME")

client = AsyncIOMotorClient(MONGO_URI)

def get_database():
    return client[DB_NAME]

# db = get_database()
