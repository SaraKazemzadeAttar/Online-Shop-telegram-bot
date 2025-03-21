# from pymongo import MongoClient
# from datetime import datetime

# # Connect to MongoDB
# client = MongoClient("mongodb://127.0.0.1:27017/")
# db = client["telegram_bot"] 
# users_collection = db["users"]  

# def register(bot):
#     def is_registered(user_id):
#         return users_collection.find_one({"_id": user_id}) is not None

#     def insert_user(user_id, first_name, phone=None, email=None, username=None):
#         user_data = {
#             "_id": user_id,
#             "first_name": first_name,
#             "phone": phone,
#             "email": email,
#             "username": username,
#             "created_at": datetime.utcnow()
#         }
#         users_collection.insert_one(user_data)