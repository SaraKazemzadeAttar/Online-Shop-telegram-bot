import telebot
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["telegram_bot"] 
cart_collection = db["carts"]

def register(bot):
    
    @bot.message_handler(commands=['add'])
    def add_to_cart(message):
        user_id = message.chat.id
        msg = message.text.split()

        if len(msg) < 2:
            bot.send_message(user_id, "Usage: /add <product_id>")
            return

        product = msg[1]

        cart_collection.update_one(
            {"user_id": user_id},
            {"$push": {"products": product}},
            upsert=True
        )

        bot.reply_to(message, f"✅ Product *{product}* has been added to your cart.", parse_mode="Markdown")

# remove product from cart 
    @bot.message_handler(commands=['remove'])
    def remove_from_cart(message):
        user_id = message.chat.id
        product = message.text.replace("/remove ", "").strip()

        if not product:
            bot.reply_to(message, "❌ Please enter the product name you want to remove.", parse_mode="Markdown")
            return

        cart_collection.update_one(
            {"user_id": user_id},
            {"$pull": {"products": product}}
        )

        bot.reply_to(message, f"🗑️ Product *{product}* has been removed from your cart.", parse_mode="Markdown")

# view your cart
    @bot.message_handler(commands=['review'])
    def view_cart(message):
        user_id = message.chat.id
        cart = cart_collection.find_one({"user_id": user_id})

        if not cart or "products" not in cart or len(cart["products"]) == 0:
            bot.reply_to(message, "🛒 Your cart is empty.")
            return

        cart_items = "\n".join([f"- {item}" for item in cart["products"]])
        bot.reply_to(message, f" *Your Cart:*\n{cart_items} \n Enter /confirm to buy them :)", parse_mode="Markdown")
        
