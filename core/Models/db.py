from pymongo import MongoClient
from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # This forces a connection check
    print("Connected to MongoDB!")
except Exception as e:
    print("Error:", e)

db = client["telegram_shop"]

users_collection = db["users"]
carts_collection = db["carts"]
orders_collection = db["orders"]
