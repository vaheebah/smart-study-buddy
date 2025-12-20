from pymongo import MongoClient
from pymongo.database import Database
from app.config import settings

client = MongoClient(settings.MONGO_URL)
db: Database = client[settings.MONGO_DB_NAME]

def get_mongo_db() -> Database:
    return db
