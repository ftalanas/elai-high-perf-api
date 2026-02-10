import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

# Struttura DB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "elai")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "predictions")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


# Salvataggio predizione su DB
async def save_prediction(input_data, output_data, n_records: int, mode: str):
    doc = {
        "timestamp": datetime.now(timezone.utc),
        "mode": mode,
        "n_records": n_records,
        "input_data": input_data,
        "output_data": output_data,
    }
    await collection.insert_one(doc)
