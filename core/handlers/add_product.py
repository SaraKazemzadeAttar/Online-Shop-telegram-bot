import telebot

def register(bot):
        
    @bot.message_handler(commands=['add'])
    def add_to_cart(message):
        user_id = message.chat.id
        msg = message.text.split()

        if len(msg) < 3:
            bot.send_message(user_id, "Usage: /add <product_id> <quantity>")
            return

        product_id = msg[1]
        quantity = int(msg[2])

        carts_collection.update_one({"user_id": user_id}, {"$push": {"items": {"product_id": product_id, "quantity": quantity}}}, upsert=True)
        bot.send_message(user_id, f"✅ Added {quantity} of Product {product_id} to your cart!")

