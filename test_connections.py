import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("TESTING SMART STUDY BUDDY CONNECTIONS")

# Test PostgreSQL
print("\n[1] Testing PostgreSQL Connection...")
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("     PostgreSQL Connected Successfully!")
except Exception as e:
    print(f"     PostgreSQL Error: {e}")

# Test MongoDB
print("\n[2] Testing MongoDB Connection...")
try:
    from pymongo import MongoClient
    client = MongoClient(os.getenv('MONGO_URL'), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("     MongoDB Connected Successfully!")
except Exception as e:
    print(f"    MongoDB Error: {e}")

# Test OpenAI API
print("\n[3] Testing OpenAI API Connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # Make a test call
    response = client.models.list()
    print("     OpenAI API Connected Successfully!")
except Exception as e:
    print(f"     OpenAI API Error: {e}")


print("CONNECTION TEST COMPLETE")
