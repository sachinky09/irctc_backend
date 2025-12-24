# irctc_backend/mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5s timeout
    db = client["irctc"]
    mongo_collection = db["train_search_logs"]

    # Test connection
    client.server_info()  # Will raise exception if cannot connect
    print("MongoDB connection successful!")

except Exception as e:
    mongo_collection = None
    print("MongoDB connection failed:", e)
