import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('MONGODB_DB', 'student_predictor')

client = None
collection = None

if MONGODB_URI:
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db['predictions']

async def save_prediction(doc: dict):
    if collection is None:
        raise RuntimeError('MongoDB not configured. Set MONGODB_URI.')
    result = await collection.insert_one(doc)
    return result.inserted_id

async def get_history(limit: int = 100):
    if collection is None:
        raise RuntimeError('MongoDB not configured. Set MONGODB_URI.')
    cursor = collection.find().sort('timestamp', -1).limit(limit)
    rows = []
    async for item in cursor:
        item['_id'] = str(item['_id'])
        rows.append(item)
    return rows
